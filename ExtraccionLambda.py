import schedule
import time
from apify_client import ApifyClient
from pysentimiento import create_analyzer
import sys
#Permite al sistema imprimir caracteres especiales
sys.stdout.reconfigure(encoding='utf-8')

def lambda_scrapper(username):

    # Inicializa el cliente de apify con el token de autenticación
    client = ApifyClient("<TOKEN APIFY>")

    # Input para realizar la llamada al Actor
    run_input = {
        "username": [username],
        "resultsLimit": 10,
    }

    # Corre el actor que extraerá la información
    run = client.actor("apify/instagram-post-scraper").call(run_input=run_input)

    # Extrae y guarda la información en una lista
    captions = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        captions.append(item.get('caption'))

    #Se declara el analizador de sentimiento
    analyzer = create_analyzer(task="sentiment", lang="es")

    #Realiza análisis de sentimiento
    results = analyzer.predict(captions)

    print(results)

    return captions, results


"""# Programar la ejecución de la función lambda_handler cada 24 horas
schedule.every(24).hours.do(lambda_scrapper("unijaveriana"))

# Ejecutar el bucle de planificación
while True:
    schedule.run_pending()
    time.sleep(1)"""

lambda_scrapper("unijaveriana")


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