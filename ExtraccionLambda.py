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
apifyToken = "<API>"

#Declaramos token de Apify 
clientApify = ApifyClient(apifyToken)

# Crea un nuevo cliente y se contecta al servidor
clientMongo = MongoClient(mongoUri, server_api=ServerApi('1'))

# Se conecta a la base de datos
db = clientMongo.datosRedesSociales

# Utilizamos la colección "datos"
collection = db["Entries"]

# Función para guardar datos en MongoDB desde Python, recibe una lista de objetos json
def guardar_datos_en_mongo(datos):
    try:
        for obj in datos:
            # Insertar el objeto JSON en la base de datos
            collection.insert_one(obj)
        
        return 'Datos guardados correctamente en MongoDB.'

    except Exception as e:
        return 'Error al guardar los datos en MongoDB:', e 


#Función lambda que extrae la información de un usuario de Instagram 
def lambda_handler_ig(event, context): 

    # Recogemos el nombre del usuario de instagram a buscar de event[user]
    username = event.get("username")

    # Formato fecha = YYYY-MM-DD
    date_until_search = event.get("date_until_search")

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

    datos = []
    for item in clientApify.dataset(run["defaultDatasetId"]).iterate_items():
        tipo = item.get("type")

        if tipo == "Video":
            mediaURL = [item.get("videoUrl")]

        if tipo == "Sidecar":
            mediaURL = item.get("images")

        if tipo == "Image":
            mediaURL = [item.get("displayUrl")]

        # Convierte los datos en un objeto JSON
        objeto_json = {
            "type":"post de Instagram",
            "socialNetwork": "instagram",
            "content": item.get("caption"),
            "usernameSocialNetwork": username,
            "dateCreated": item.get("timestamp"),
            "dateQuery":datetime.now(),
            "location": item.get("locationName"),
            "usersMentioned": item.get("mentions"),
            "properties":{
                "postId":item.get("id"),
                "postURL":item.get("url"),
                "mediaURL":mediaURL,
                "likes":item.get("likesCount"),
                "comments":item.get("commentsCount")
            },
            "_parentEntryID":item.get("ownerId"),
            "hashtags": item.get('hashtags')
        }
        datos.append(objeto_json)
    
    result = {"response": guardar_datos_en_mongo(datos)}
    return result

#Función lambda que extrae la información de un usuario de Facebook
def lambda_handler_fb(event, context): 

    # Recogemos el nombre del usuario de facebook a buscar de event[user]
    username = event.get("username")

    # Formato fecha = YYYY-MM-DD
    date_until_search = event.get("date_until_search")

    # Obtenemos el número máximo de posts a buscar
    max_posts = event.get("max_posts")
    
    if not username:
        return {"response": "No se proporciona nombre de usuario"}
    
    if not date_until_search:
        date_until_search = "2023-12-24"
    if not max_posts:
        max_posts=10


    run_input = {
        "afterTime": date_until_search,
        "max_results": max_posts,
        "profile_urls": [
            {
                "url": "https://www.facebook.com/"+username+"/"
            }
        ]
    }

    # Corre el actor que extraerá la información
    run = clientApify.actor("iKRDqb590bAYWxy4q").call(run_input=run_input)

    datos = []
    for item in clientApify.dataset(run["defaultDatasetId"]).iterate_items():
        # Convierte los datos en un objeto JSON
        objeto_json = {
            "type":"post de Facebook",
            "socialNetwork": "facebook",
            "content": item.get("caption"),
            "usernameSocialNetwork": username,
            "dateCreated": item.get("post_date"),
            "dateQuery":datetime.now(),
            "properties":{
                "postId":item.get("post_id"),
                "postURL":item.get("post_url"),
                "mediaURL":item.get("media_url"),
                "likes":item.get("likesCount"),
                "comments":item.get("total_comment_count"),
                "reactions":item.get("total_reactions"),
                "shares":item.get("share_count"),
            },
            "_parentEntryID":item.get("ownerId"),
            #"hashtags": item.get('hashtags')
        }
        datos.append(objeto_json)
    
    result = {"response": guardar_datos_en_mongo(datos)}
    return result

event={
    "username":"gustavopetrourrego",
    "date_until_search":"2023-12-24",
    "max_posts": 3
}

print(lambda_handler_ig(event, None))
