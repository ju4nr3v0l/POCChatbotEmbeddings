# POC chatbot creado por juan marulanda utilizando embeddings de OpenAI

## Instalación
    - Instalar Redis
    - Instalar Python 3.6
    - Instalar dependencias
        - Dependencias:
            - flask
            - numpy
            - openai
            - time
            - os
            - dotenv
    - Crear arhivo .env con la siguiente estructura:
```
API_KEY=YOUR-OPEAIN-API-KEY
REDIS_HOST=HOST-REDIS-URL
REDIS_PORT=REDIS-PORT
```
    - Correr el archivo maint.py

## Consideraciones
En el archivo functions.py se encuentra la función que se encarga de hacer la petición a la API de OpenAI, 
en esta funcion se encuentra en listado de palabras que estara parametrizado en la construccion de los vectores
multidimensionales de los embeddings.

Se uso el modelo [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings).

Redis actua como un middleware que permite guardar dichos vectores y antes de realizar cualquier peticion, se
consulta esta base de datos, permitiendo asi, reducir el tiempo de respuesta de la API de OpenAI y ahorrar dinero.
