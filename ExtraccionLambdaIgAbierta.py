"""
@Author: Gabriel Martín
"""
from apify_client import ApifyClient
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import json
import re
import os

#Permite al sistema imprimir caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')

#uri de conexión a Mongo (ingresa tu propia uri)
mongoUri = os.environ["MONGOURI"]
    
#Apify token (Ingresa el token de tu cuenta de Apify)
apifyToken = os.environ["APIFYKEY"]

#Función para comprobar si una fecha es posterior a la fecha actual
def es_fecha_despues_de_hoy(fecha):
    try:
        fecha_entrada = datetime.strptime(fecha, '%Y-%m-%d')
        hoy = datetime.now()
        return fecha_entrada > hoy
    except ValueError:
        print("Formato de fecha incorrecto. Utiliza el formato AAAA-MM-DD.")
        return False

# Función para guardar datos en MongoDB desde Python, recibe una lista de objetos json
def guardar_datos_en_mongo(datos):
    try:

        # Crea un nuevo cliente y se contecta al servidor
        clientMongo = MongoClient(mongoUri, server_api=ServerApi('1'))

        # Se conecta a la base de datos
        db = clientMongo.datosRedesSociales

        # Utilizamos la colección "datos"
        collection = db["Entries"]

        for obj in datos:
            # Insertar el objeto JSON en la base de datos
            collection.insert_one(obj)
        
        return 'Datos guardados correctamente en MongoDB.'

    except Exception as e:
        return 'Error al guardar los datos en MongoDB:', str(e) 

#Función que extrae los hashtags y menciones de un texto    
def extract_hashtags_mentions(text):
    # Define los patrones de las expresiones regulares para hashtags y menciones
    hashtag_pattern = r'#(\w+)'  # Hashtags: palabras que comienzan con '#'
    mention_pattern = r'@(\w+)'  # Menciones: palabras que comienzan con '@'
    
    # Encuentra todos los hashtags y menciones en el texto
    hashtags = re.findall(hashtag_pattern, text)
    mentions = re.findall(mention_pattern, text)
    
    # Devuelve un diccionario con los hashtags y menciones
    result = {
        "hashtags": hashtags,
        "mentions": mentions
    }
    
    return result
    
#Función que extrae los primeros 50 comentarios de un post dado
def extraccion_comentarios_ig(padre, urls, num_comentarios):
    run_input={
        "addParentData": False,
        "directUrls": urls,
        "enhanceUserSearchWithFacebookPage": False,
        "isUserTaggedFeedURL": False,
        "resultsLimit": num_comentarios,
        "resultsType": "comments",
        "searchType": "hashtag"
    }


    try:

        #Declaramos token de Apify 
        clientApify = ApifyClient(apifyToken)

        # Run the Actor and wait for it to finish
        run = clientApify.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

        #Lista donde se guardarán los comentarios
        datos = []

        #Contador para determinar iteración
        it = 0

        #Contador para determinar en qué post se está ubicado
        cont_p = 0

        # Fetch and print Actor results from the run's dataset (if there are any)
        for item in clientApify.dataset(run["defaultDatasetId"]).iterate_items():
            
            if not item.get("error"):
                datos_e = extract_hashtags_mentions(item.get("text"))
                # Convierte los datos en un objeto JSON
                objeto_json = {
                    "type":"comentario de Instagram",
                    "socialNetwork": "instagram",
                    "content": item.get("text"),
                    "usernameSocialNetwork": item.get("ownerUsername"),
                    "dateCreated": str(item.get("timestamp")),
                    "dateQuery":str(datetime.now()),
                    "location": "null",
                    "usersMentioned": datos_e.get("mentions"),
                    "properties":{
                        "postId":item.get("id"),
                        "postURL":"No contiene",
                        "mediaURL":"No contiene",
                        "likes":item.get("likesCount"),
                        "comments":"No aplica"
                    },
                    "_parentEntryID":padre[cont_p].get("properties").get("postId"),
                    "hashtags": datos_e.get('hashtags')
                }

                # Agrega el objeto JSON a la lista
                datos.append(objeto_json)
            it+=1
            
            #Se pasa al siguiente post cuando ya se extrajo el número de comentarios indicado para cada post
            if it % num_comentarios == 0:
                cont_p+=1 
        
        return {"response": guardar_datos_en_mongo(datos)}
    
    except Exception as e:
        return {"response": "Error: " + str(e)}
    
def extraer_posts(posts, busqueda, max_comments):

    #Lista de posts a guardar
    datos = []

    #Lista de URLs
    urls = []

    #Lista de posts con comentarios
    posts_con_comentarios = []

    for item in posts:
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
            "search": busqueda,
            "dateCreated": str(item.get("timestamp")),
            "dateQuery":str(datetime.now()),
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
        if item.get("commentsCount") > 0:
            urls.append(str(item.get("url")))
            posts_con_comentarios.append(objeto_json)
        datos.append(objeto_json)
    
    #Extrae los comentarios de los posts
    extraccion_comentarios_ig(posts_con_comentarios,urls,max_comments)

    #Revisa que se hayan podido extraer datos del perfil
    if len(datos) == 0:
        return {"response": "No se encontraron resultados asociados a la búsqueda"}

    return {"response": guardar_datos_en_mongo(datos)}

#Función lambda que extrae la información de un usuario de Instagram 
def lambda_handler(event, context): 

    # Recogemos el nombre del usuario de instagram a buscar de event[user]
    busqueda = event.get("search")

    # Formato fecha = YYYY-MM-DD
    date_until_search = event.get("date_until_search")

    # Obtenemos el número máximo de posts a buscar
    max_posts = event.get("max_posts")

    # Obtenemos el número máximo de comentarios a buscar
    max_comments = event.get("max_comments")
    
    #Comprobaciones de campos faltantes
    if not busqueda:
        return {"response": "No se proporciona busqueda a realizar"}
    if not date_until_search:
        return {"response": "No se proporciona fecha máxima"}
    if not max_posts:
        return {"response": "No se proporciona máximo de posts"}
    if not max_comments:
        return {"response": "No se proporciona máximo de comentarios"}

    #Comprueba si la fecha es posterior a la actual
    if es_fecha_despues_de_hoy(date_until_search):
        return {"response": "Fecha incorrecta. La fecha debe ser anterior a la fecha actual"}

    run_input = {
        "addParentData": False,
        "enhanceUserSearchWithFacebookPage": False,
        "isUserTaggedFeedURL": False,
        "onlyPostsNewerThan": date_until_search,
        "resultsLimit": 10,
        "resultsType": "posts",
        "search": busqueda,
        "searchLimit": 10,
        "searchType": "hashtag"
}

    #Se prueba la conexión a la base de datos antes de ejecutar el actor
    try:
        #Intenta llamar a la base de datos
        clientMongo = MongoClient(mongoUri, server_api=ServerApi('1'))
        
        # Se conecta a la base de datos
        db = clientMongo.datosRedesSociales

        # Utilizamos la colección "datos"
        collection = db["Entries"]
        insert_result= collection.insert_one({"":""})
        
        # Obtener el ID del registro insertado
        inserted_id = insert_result.inserted_id

        # Eliminar el registro recién insertado
        collection.delete_one({"_id": inserted_id})
    
    except Exception as e:
        return {"response": "Error: " + str(e)}

    try:
        #Declaramos token de Apify 
        clientApify = ApifyClient(apifyToken)

        # Corre el actor que extraerá la información
        run = clientApify.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)

        #Lista de resultados encontrados
        datos = []

        for item in clientApify.dataset(run["defaultDatasetId"]).iterate_items():
            datos.append(item)

        #Revisa que se hayan encontrado resultados
        if len(datos) == 0:
            return {"response": "No se encontraron resultados asociados a la búsqueda"}

        return extraer_posts(datos[2].get("latestPosts")[:max_posts], busqueda, max_comments)
    
    except Exception as e:
        return {"response": "Error" + str(e)}

