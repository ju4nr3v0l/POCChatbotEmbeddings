import time
import os
import re
import openai
from redis_client import RedisClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
openai.api_key = os.getenv('API_KEY')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

dir_path = 'md'
files_pattern = '*.md'
files_to_read = os.listdir(dir_path)

def split_text(file):
    separator = "\n### "
    return file.split(separator)

def get_title(file):
    match = re.search(r"title:\s+(.+)\s+", file)
    if match:
        title = match.group(1)
        return title
    else:
        " "

def create_embedding(text):
    redis_client = RedisClient(host=redis_host, port=redis_port)
    time.sleep(1)
    for txt in text:
        key = txt
        if not redis_client.exists(key):
            print("creating embedding for: " + txt)
            response = openai.Embedding.create(
                input=txt,
                model="text-embedding-ada-002"
            )
            embeddings = response['data'][0]['embedding']
            redis_client.set(key, embeddings)


def remove_header(page_md):
    md_lines = page_md.split("\n")

    body_lines = []
    in_body = False
    for mdl in md_lines:
        if len(mdl) > 0 and mdl[0] == "#":
            in_body = True
        if in_body:
            body_lines.append(mdl)
    page_md = "\n".join(body_lines)
    return page_md


def remove_line_numbers(page_md):
    lines = page_md.split('\n')
    lines = [
        re.sub(r'^\s*\d+\s*', '', line)
        for line in lines
    ]

    page_md = '\n'.join(lines)
    return page_md


def remove_table_rows(page_md):
    lines = page_md.split('\n')
    lines = [line
             for line in lines
             if len(line) == 0 or not set(line).issubset(set("| -"))
             ]
    page_md = '\n'.join(lines)
    return page_md


def remove_extra_newlines(page_md):
    page_md = re.sub(r'\n{3,}', '\n\n', page_md)
    return page_md


def remove_unicode(page_md):
    for uchar in ["\u2500", "\u2514", "\u251c", "\u2502"]:
        page_md = page_md.replace(uchar, "")
    for uchar in ["\u2588", "\u2019"]:
        page_md = page_md.replace(uchar, "'")
    for uchar in ["\u201d", "\u201c"]:
        page_md = page_md.replace(uchar, "\"")
    page_md = page_md.replace("\u00a9", "copyright")
    return page_md


def remove_bolding(page_md):
    page_md = page_md.replace("**", "")
    return page_md


def remove_empty_code_blocks(page_md):
    parts = page_md.split('```')
    parts = [
        p
        for i, p in enumerate(parts)
        if i % 2 == 0 or p != "\n"
    ]
    return "```".join(parts)


################################################################

def remove_links(page_md):
    match = re.search('\[.*?\]\(.*?\)', page_md)
    if match is not None:
        start, end = match.span()
        link = page_md[start:end]
        link_text = link[1:].split(']')[0]
        if link_text != "¶":
            return page_md[:start] + link_text + remove_links(page_md[end:])
        else:
            return page_md[:end] + link + remove_links(page_md[end:])
    return page_md


def remove_images(page_md):
    return re.sub('!\[\]\(data:image\/png;base64.*?\)', '', page_md)


def remove_jupyter_widgets(page_md):
    lines = page_md.split('\n')
    lines = [
        line
        for line in lines
        if len(line) == 0 or (line[0] != "{" and "jupyter-widgets" not in line)
    ]
    return "\n".join(lines)


def remove_xml(page_md):
    lines = page_md.split('\n')
    lines = [line for line in lines if not line.startswith('<?xml')]
    return "\n".join(lines)


def reformat_markdown(page_md):
    page_md = page_md.replace("\_", "_").replace("\*", "*")
    page_md = remove_links(page_md)
    page_md = remove_images(page_md)
    page_md = remove_jupyter_widgets(page_md)
    page_md = remove_xml(page_md)
    return page_md

for file in files_to_read:
    print("processing file: " + file)
    #markdown_text = file.read_text()
    file_to_read = open(Path(dir_path + '/' + file)).read()
    file_to_read = remove_header(file_to_read)
    #file_to_read = remove_footer(file_to_read)
    file_to_read = remove_line_numbers(file_to_read)
    file_to_read = remove_table_rows(file_to_read)
    file_to_read = remove_extra_newlines(file_to_read)
    file_to_read = remove_empty_code_blocks(file_to_read)
    file_to_read = remove_extra_newlines(file_to_read)
    file_to_read = remove_bolding(file_to_read)
    file_to_read = remove_unicode(file_to_read)

    ### reformat now that the markdown is clean
    file_to_read = reformat_markdown(file_to_read)
    #markdown_text = file_to_read.read_text()
    chunks = split_text(file_to_read)
    document_title = get_title(file_to_read)
    create_embedding(chunks)
    #file_to_read.close()




