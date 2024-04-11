"""
@Author: Gabriel Martín
"""
from apify_client import ApifyClient
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

#Permite al sistema imprimir caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')

#uri de conexión a Mongo (ingresa tu propia uri)
mongoUri = "<URI>"

#Apify token (Ingresa el token de tu cuenta de Apify)
apifyToken = "<TOKEN>"

#Declaramos token de Apify 
clientApify = ApifyClient(apifyToken)

# Crea un nuevo cliente y se contecta al servidor
clientMongo = MongoClient(mongoUri, server_api=ServerApi('1'))

# Se conecta a la base de datos
db = clientMongo.datosRedesSociales

# Utilizamos la colección "datos"
collection = db["Entries"]

# Función para guardar datos en MongoDB desde Python
def guardar_datos_en_mongo(objeto_json):
    try:
        # Añadir el atributo dateQuery
        objeto_json['dateQuery'] = datetime.now()

        # Insertar el objeto JSON en la base de datos
        collection.insert_one(objeto_json)
        
        return 'Datos guardados correctamente en MongoDB.'

    except Exception as e:
        return 'Error al guardar los datos en MongoDB:', e 


#Función lambda que extrae la información de un usuario de Instagram 
def lambda_handler(event, context): 

    # Recogemos el nombre del usuario de instagram a buscar de event[user]
    username = event.get("username")

    # Formato fecha = YYYY-MM-DD
    date_until_search = event.get("date")

    # Obtenemos el número máximo de posts a buscar
    max_posts = event.get("max_posts")
    
    if not username:
        return {"response": "No se proporciona nombre de usuario"}
    
    if not date_until_search:
        date_until_search = "2023-12-24"
    if not max_posts:
        max_posts=10


    run_input = {
        "addParentData": False,
        "directUrls": [
        "https://www.instagram.com/"+username+"/",
        ],
        "enhanceUserSearchWithFacebookPage": False,
        "isUserTaggedFeedURL": False,
        "onlyPostsNewerThan": date_until_search,
        "resultsLimit": max_posts,
        "resultsType": "posts"
    }

    # Corre el actor que extraerá la información
    run = clientApify.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

    for item in clientApify.dataset(run["defaultDatasetId"]).iterate_items():
        # Convierte los datos en un objeto JSON
        objeto_json = {
            "username": username,
            "captions": item.get("caption"),
        }

        result = {"response": guardar_datos_en_mongo(objeto_json)}

    return result

event={
    "username":"gustavopetrourrego",
    "date_until_search":"2021-05-06",
    "max_posts": 10
}

lambda_handler(event, None)

"""
@misc{perez2021pysentimiento,
      title={pysentimiento: A Python Toolkit for Opinion Mining and Social NLP tasks}, 
      author={Juan Manuel Pérez and Mariela Rajngewerc and Juan Carlos Giudici and Damián A. Furman and Franco Luque and Laura Alonso Alemany and María Vanina Martínez},
      year={2023},
      eprint={2106.09462},a
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""
