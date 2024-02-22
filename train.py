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

def create_embedding(text):
    print("creating embedding for: " + text)
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']


def get_embedding_answers(text):
    redis_client = RedisClient(host=redis_host, port=redis_port, db=1)
    key = text
    if not redis_client.exists(key):
        time.sleep(1)
        embeddings = create_embedding(text)
        redis_client.set(key, embeddings)
    else:
        embeddings = redis_client.get(key)
    print(embeddings)
    return embeddings


def create_answer_base():
    text_list = ["sistecredito es una empresa que le dice si a los que les dicen no",
                 "para solicitar tu credito solo debes tener tu cedula y una camara",
                 "tienes un cupo maximo de $3.000.000 para que lo disfrutes",
                 "comparas minimas desde $10.000",
                 "la cantidad de cuotas maximas es de 12 cuotas mensuales",
                 "si pagas antes de 1 mes tus cuotas no te cobramos interes ni cargos extra!",
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
                 "Luisa es una muy buena trabajadora",
                 "cordial saludo\nEs un gusto atender tu solicitud de información\nPara conocer la información de tu crédito, ingresa a nuestra página web www.sistecredito.com inicia sesión en la zona de acceso a Personas con tu usuario y contraseña. Si no tienes un usuario y contraseña puedes registrarte allí mismo.\nSi presentas dudas con el estado de tu crédito, llámanos o escríbenos al número celular 3208899898\nEsperamos haber dado respuesta a tu solicitud y agradecemos tu comunicación con nosotros."
                 ]
    for text in text_list:
        get_embedding_answers(text)

create_answer_base()