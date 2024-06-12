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
def extraccion_comentarios_fb(padre, urls, num_comentarios):
    run_input={
        "includeNestedComments": False,
        "resultsLimit": num_comentarios,
        "startUrls": urls,
        "viewOption": "RANKED_UNFILTERED"   
    }

    try:
        #Declaramos token de Apify 
        clientApify = ApifyClient(apifyToken)

        # Run the Actor and wait for it to finish
        run = clientApify.actor("us5srxAYnsrkgUv2v").call(run_input=run_input)

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
                    "type":"comentario de Facebook",
                    "socialNetwork": "facebook",
                    "content": item.get("text"),
                    "usernameSocialNetwork": padre[cont_p].get("pageName"),
                    "dateCreated": str(item.get("date")),
                    "dateQuery":str(datetime.now()),
                    "location": "null",
                    "usersMentioned": datos_e.get("mentions"),
                    "properties":{
                        "postId":item.get("id"),
                        "postURL":item.get("commentUrl"),
                        "mediaURL":"No contiene",
                        "likes":item.get("likesCount"),
                        "comments":"No aplica"
                    },
                    "_parentEntryID":padre[cont_p].get("postId"),
                    "hashtags": datos_e.get('hashtags')
                }
                datos.append(objeto_json)
                it+=1
            else:
                it = num_comentarios
            
            #Se pasa al siguiente post cuando ya se extrajo el número de comentarios indicado para cada post
            if it % num_comentarios == 0:
                cont_p+=1 
        
        result = {"response": guardar_datos_en_mongo(datos)}
        return result
    
    except Exception as e:
        return {"response": "Error: " + str(e)}

#Función lambda que extrae la información de un usuario de Instagram 
def lambda_handler(event, context): 

    # Recogemos el nombre del usuario de instagram a buscar de event[user]
    search = event.get("search")

    # Formato fecha = YYYY-MM-DD
    date_until_search = event.get("date_until_search")

    # Obtenemos el número máximo de posts a buscar
    max_posts = event.get("max_posts")
    
    #Comprobaciones de campos faltantes
    if not search:
        return {"response": "No se proporciona búsqueda a realizar"}
    if not date_until_search:
        return {"response": "No se proporciona fecha máxima"}
    if not max_posts:
        return {"response": "No se proporciona máximo de posts"}
    
    #Comprueba si la fecha es posterior a la actual
    if es_fecha_despues_de_hoy(date_until_search):
        return {"response": "Fecha incorrecta. La fecha debe ser anterior a la fecha actual"}

    run_input = {
        "keywordList":search,
        "resultsLimit": max_posts
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
        run = clientApify.actor("qgl7gVMdjLUUrMI5P").call(run_input=run_input)

        #Lista de posts a guardar
        datos = []

        #Lista de URLs
        urls = []

        #Lista de posts con comentarios
        posts_con_comentarios = []

        for item in clientApify.dataset(run["defaultDatasetId"]).iterate_items():

            if not item.get("error"):
                # Extraemos las menciones y hashtags del caption
                datos_e_e = extract_hashtags_mentions(item.get("text"))

                #Comprobar que el post tiene imágenes o videos y guardarlas en la variable uri_value
                media_data = item.get("attachments")
                if media_data:
                    uri_value = [item["thumbnail"] for item in media_data]
                else:
                    uri_value = "Sin contenido"

                # Convierte los datos en un objeto JSON
                objeto_json = {
                    "type":"post de Facebook",
                    "socialNetwork": "facebook",
                    "content": item.get("text"),
                    "usernameSocialNetwork":item.get("user").get("name"),
                    "search": search,
                    "dateCreated": str(item.get("date")),
                    "dateQuery":str(datetime.now()),
                    "usersMentioned": datos_e_e.get("mentions"),
                    "properties":{
                        "postId":item.get("postId"),
                        "postURL":item.get("url"),
                        "mediaURL":uri_value,
                        "comments":item.get("commentsCount"),
                        "reactions":item.get("likesCount"),
                        "shares":item.get("sharesCount"),
                        "views":item.get("viewsCount"),
                    },
                    "_parentEntryID":item.get("user").get("id"),
                    "hashtags": datos_e_e.get("hashtags")
                }
                if item.get("commentsCount") > 0:
                    urls.append(str(item.get("url")))
                    posts_con_comentarios.append(item)

                datos.append(objeto_json)

        #Extrae los comentarios de los posts
        extraccion_comentarios_fb(posts_con_comentarios,urls,50)

        #Revisa que se hayan podido extraer datos del perfil
        if len(datos) == 0:
            return {"response": "No se pudieron extraer datos del perfil"}
        
        return {"response": guardar_datos_en_mongo(datos)}

    except Exception as e:
        return {"response": "Error: " + str(e)}

