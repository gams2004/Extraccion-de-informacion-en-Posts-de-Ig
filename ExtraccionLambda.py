"""
@Author: Gabriel Martín
"""
from apify_client import ApifyClient
from pysentimiento import create_analyzer
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

#Permite al sistema imprimir caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')

#uri de conexión a Mongo (ingresa tu propia uri)
uri = "<URI>"

#Declaramos token de Apify (Ingresa el token de tu cuenta de Apify)
client = ApifyClient("<TOKEN APIFY>")

# Crea un nuevo cliente y se contecta al servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Se conecta a la base de datos
db = client.datosRedesSociales

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


#Función lambda que obtiene el sentimiento de los posts de Instagram de un usuario dado
obtener_datos_instagram = lambda username : {
    #Devuelve una lista con las descripciones de los posts
  "descripciones": guardar_datos_en_mongo(
      objeto_json={ 
          "descripciones": client.dataset(client.actor("apify/instagram-post-scraper").call(run_input={"username": [username],"resultsLimit": 10})["defaultDatasetId"])[0].get('caption')
      })
    }

# Programar la ejecución de la función lambda_handler cada 24 horas
obtener_datos_instagram("unijaveriana")

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
