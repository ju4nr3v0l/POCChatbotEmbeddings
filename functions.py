import numpy as np
import openai
import time
from redis_client import RedisClient
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('API_KEY')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')


# retrieve the embedding from the redis cache
# if it doesn't exist, create it and store it in the cache
# then return it
def get_embedding(text):
    redis_client = RedisClient(host=redis_host, port=redis_port)
    key = text
    if not redis_client.exists(key):
        time.sleep(1)
        print("creating embedding for: " + text)
        response = openai.Embedding.create(
            input=text,
            model = "text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        redis_client.set(key, embeddings)
    else:
        embeddings = redis_client.get(key)
    return embeddings

# calculate the cosine similarity between two embeddings
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# calculate the similarity between two texts
def similarity(text1, text2):
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    return cosine_similarity(embedding1, embedding2)

# calculate the similarity between a text and a list of texts
def similarity_list(text, text_list):
    embedding1 = get_embedding(text)
    similarities = []
    for text2 in text_list:
        embedding2 = get_embedding(text2)
        similarities.append(cosine_similarity(embedding1, embedding2))
    return similarities

# calculate the similarity between a text and a list of texts
# and return the most similar text
def most_similar(text):
    text_list = ["sistecredito es una empresa que le dice si a los que les dicen no",
                 "para solicitar tu credito solo debes tener tu cedula y una camara",
                 "tienes un cupo maximo de $3.000.000 para que lo disfrutes",
                 "comparas minimas desde $10.000",
                 "la cantidad de cuotas maximas es de 12 cuotas mensuales",
                 "si pagas antes de 1 mens tus cuotas no te cobramos interes ni cargos extra!",
                 "Trabajo en la inmobiliaria Alberto Alvarez.",
                 "Atender a los clientes para que tengan una experiencia increible.",
                 "por favor ingresa a esta url https://albertoalvarez.com/wp-content/uploads/2022/02/requisitos-para-arrendar-con-aa.pdf",
                 "Claro! en esta pagina puedes encontrar muchos proyectos de tu interes https://albertoalvarez.com/proyectos/",
                 "Inmobiliaria Alberto Alvarez por supuesto", "nuestro numero de atencion es 318 5668227",
                 "en nuestra pagina https://albertoalvarez.com puedes encontrar todos nuestros datos de contacto",
                 "por que somos los mejores del sector inmobiliario en colombia",
                 "Trabajamos con las mejores tecnologias asesorados por JADI SAS",
                 "por uspuesto, acercate a nuestras oficinas para atenderte como te mereces",
                 "Rodas es la persona mas GAY del mundo",
                 "Luisa es una muy buena trabajadora"]

    similarities = similarity_list(text, text_list)
    return text_list[similarities.index(max(similarities))]

# calculate the similarity between a text and a list of texts
# and return the most similar text and its similarity
def most_similar_with_similarity(text, text_list):
    similarities = similarity_list(text, text_list)
    return text_list[similarities.index(max(similarities))], max(similarities)

# calculate the similarity between a text and a list of texts
# and return the most similar text and its similarity
# if the similarity is below a threshold, return None
def most_similar_with_similarity_threshold(text, text_list, threshold):
    similarities = similarity_list(text, text_list)
    max_similarity = max(similarities)
    if max_similarity < threshold:
        return None, max_similarity
    return text_list[similarities.index(max_similarity)], max_similarity



