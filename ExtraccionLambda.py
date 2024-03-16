import schedule
import time
from apify_client import ApifyClient
from pysentimiento import create_analyzer
import sys
#Permite al sistema imprimir caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')

#Función lambda que obtiene el sentimiento de los posts de Instagram de un usuario dado
obtener_sentimientos_instagram = lambda username : {
    #Se itera por los posts del usuario y se genera el análisis 
  "analisis": create_analyzer(task="sentiment", lang="es").predict(
    [item.get('caption') for item in client.dataset(client.actor("apify/instagram-post-scraper").call(run_input={"username": [username],"resultsLimit": 10})["defaultDatasetId"]).iterate_items()]),
    
    #Devuelve una lista con las descripciones de los posts
  "descripciones":[item.get('caption') for item in client.dataset(client.actor("apify/instagram-post-scraper").call(run_input={"username": [username],"resultsLimit": 10})["defaultDatasetId"]).iterate_items()]
    }


#Declaramos token de Apify
client = ApifyClient("<TOKEN API>")

# Programar la ejecución de la función lambda_handler cada 24 horas
schedule.every(24).hours.do(obtener_sentimientos_instagram("unijaveriana"))

# Ejecutar el bucle de planificación
while True:
    schedule.run_pending()
    time.sleep(1)


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


"""lambda_scrapper = lambda username : (lambda captions, results: (captions, results))

    # Inicializa el cliente de apify con el token de autenticación
    client = ApifyClient("apify_api_pfpeKhmFpP8zbELUuRdSFmjf6F4fKs4wwUw8")

    # Extrae y guarda la información en una lista
    captions = []
    for item in client.dataset(client.actor("apify/instagram-post-scraper").call(run_input={"username": [username],"resultsLimit": 10})["defaultDatasetId"]).iterate_items():
        captions.append(item.get('caption'))

    #Se declara el analizador de sentimiento
    create_analyzer(task="sentiment", lang="es").predict(captions)
"""