import schedule
import time
from instascrape import *
from pysentimiento import sentiment

def lambda_handler():
    # Obtener el perfil de Instagram
    profile = Profile('https://www.instagram.com/confesiones___javeriana/')
    profile.scrape()
    
    # Extraer texto de los posts
    posts_text = [post['text'] for post in profile.get_posts()]
    
    # Realizar análisis de sentimientos
    sentiment_analyzer = sentiment()
    results = sentiment_analyzer.analyze(posts_text)
    
    # Retornar los resultados (o hacer algo con ellos)
    print(results)
    

# Programar la ejecución de la función lambda_handler cada 24 horas
schedule.every(20).seconds.do(lambda_handler)

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