# Extracción de información en Posts de Instagram y Facebook
Proyecto en Python, integrado con AWS Lambda, que extraerá información de los posts y comentarios de un perfil o resultados de una búsqueda abierta de Instagram y Facebook con los actores de Apify:
- [Instagram Post Scraper](https://apify.com/apify/instagram-post-scraper/api/client/python)
- [Facebook Post Scraper](https://apify.com/apify/facebook-posts-scraper)
- [Facebook Comments Scraper](https://apify.com/apify/facebook-comments-scraper)

Además, realiza el guardado de los datos en una base de datos Mongo.

Librerías utilizadas para el proyecto:

- Pymongo
- Apify 

Es importante contar con las últimas versiones de Python y PIP para correr el proyecto sin problemas.

## Pasos de uso

- Crear una función Lambda en AWS.
- Crear una capa personalizada en la función Lambda con el archivo .zip de dependencias. *Importante*: Crear la capa con un Runtime de Python 3.12 y una arquitectura x86_64.
- Agregar las variables de ambiente *APIFYKEY* y *MONGOURI* en el apartado de configuración con tu llave de Apify y tu link de conexión a la BD Mongo.
- En configuración general de la función Lambda, cambiar el tiempo de Timeout a un valor mínimo de 10 minutos.
- Pegar el código de la función a utilizar en la función Lambda.
- Enviar un evento con los parámetros de extracción para la función Lambda con el siguiente formato:

### Búqueda por perfil
```
{
  "username": "<usuario a buscar>",
  "date_until_search": "<fecha máxima en la que se buscarán los posts>", 
  "max_posts": <número máximo de posts a buscar>,
}
```

### Búqueda abierta Instagram
```
{
  "search_term": "<busqueda a realizar>",
  "date_until_search": "<fecha máxima en la que se buscarán los posts>", 
  "max_posts": <número máximo de posts a buscar>,
  "search_type": "<tipo de busqueda a realizar>"
}
```

### Búqueda abierta Facebook
```
{
  "search": ["<lista>", "<de>", "<busquedas>", "<a>", "<realizar>"],
  "date_until_search": "<fecha máxima en la que se buscarán los posts>", 
  "max_posts": <número máximo de posts a buscar>,
  "search_type": "<tipo de busqueda a realizar>"
}
```

_La fecha máxima de búsqueda debe estar en formato: AAAA-MM_-DD_.

- El resultado de la función se guardará en la base de datos Mongo.
  
*Importante:* La base de datos de Mongo debe permitir conexiones desde cualquier dirección IP. En caso de no ser así, la función no podrá conectarse a la BD y fallará.
## Salida de datos

La función devolverá un archivo JSON con el resultado de la extracción, indicando en su valor "resultado" si la extracción fue exitosa o no. 

### Ejemplo de extracción de datos Instagram
```
{
  "_id": {
    "$oid": "662f19c24cc1b92c72ae005a"
  },
  "type": "post de Instagram",
  "socialNetwork": "instagram",
  "content": "🔴El Gobierno del Cambio, liderado por el Presidente @gustavopetrourrego, se reúne en Paipa, Boyacá, para abordar los avances y desafíos por sectores, hacer seguimiento a indicadores y evaluar el presupuesto del 2025 con el que se avanzará hacia un país más justo y en Paz, hacia la Colombia Potencia Mundial de la Vida.",
  "usernameSocialNetwork": "gustavopetrourrego",
  "dateCreated": "2024-04-28T17:42:36.000Z",
  "dateQuery": "2024-04-29 03:52:35.988178",
  "location": "Paipa , Boyaca",
  "usersMentioned": [
    "gustavopetrourrego,"
  ],
  "properties": {
    "postId": "3356333526373807984",
    "postURL": "https://www.instagram.com/p/C6UF49DPrdw/",
    "mediaURL": [
      "https://scontent.cdninstagram.com/v/t51.29350-15/440984782_1346391532673678_1059315898779624112_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent.cdninstagram.com&_nc_cat=102&_nc_ohc=UFwwnB_mcC8Q7kNvgGYAmCE&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfAc7LzRwFFkm4f0hyqrIsSmlnHxJR7ynQ72xU9zTt6bwQ&oe=6634E362&_nc_sid=10d13b",
      "https://scontent.cdninstagram.com/v/t51.29350-15/441065676_372466005752797_4605504225462133589_n.jpg?stp=dst-jpg_e35&_nc_ht=scontent.cdninstagram.com&_nc_cat=101&_nc_ohc=P5dxy5JLOqQQ7kNvgHzIeY1&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfDwQ7FMjnvnCCEnG4c4-ANH8QbhMNRIzgXULygLFcMAmA&oe=6634DFFF&_nc_sid=10d13b",
      "https://scontent.cdninstagram.com/v/t51.29350-15/441084236_1467921567480912_6003664239997486687_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent.cdninstagram.com&_nc_cat=100&_nc_ohc=8lXVBa57CJIQ7kNvgFTEd-1&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfD3l49baaTE-elQP0TSZ5O0zee_MeXYn9dq8ghXUQpMBg&oe=6634E5ED&_nc_sid=10d13b",
      "https://scontent.cdninstagram.com/v/t51.29350-15/440535565_1414936186080819_7157080497283031734_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent.cdninstagram.com&_nc_cat=103&_nc_ohc=7eLz2RfbZlIQ7kNvgEJScnM&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfAaHFHS_4OaA0KPyKmlbu9_xb9pkNy28aMXi3lnSlSLtg&oe=6634F4C8&_nc_sid=10d13b",
      "https://scontent.cdninstagram.com/v/t51.29350-15/441065677_946475617267077_1041103681185628028_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent.cdninstagram.com&_nc_cat=109&_nc_ohc=KeXyJ0WawAcQ7kNvgHQCwBf&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfCI4oAeChu7_6XQJ8REJfLPFik_Hc7AKQFVNWgWwuScSg&oe=6634D9A4&_nc_sid=10d13b",
      "https://scontent.cdninstagram.com/v/t51.29350-15/441106496_682569543939316_2434762483275276082_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent.cdninstagram.com&_nc_cat=104&_nc_ohc=hobE66CxjCEQ7kNvgGHhXkM&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfBl1wckcgUUhgSmxBorprJ7nUSzTi6A9FdKhbvAGYt4Qg&oe=6634DF1B&_nc_sid=10d13b",
      "https://scontent.cdninstagram.com/v/t51.29350-15/440999726_983240983186984_9033488128673705562_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent.cdninstagram.com&_nc_cat=104&_nc_ohc=AATy05JBOJQQ7kNvgHjIcLp&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfDxPggzXn2cnRb25-2Yr2pxr7AXuQG8JDzSHHQELDHFng&oe=6634F591&_nc_sid=10d13b",
      "https://scontent.cdninstagram.com/v/t51.29350-15/441040175_1148596239475591_8432514028929961494_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=scontent.cdninstagram.com&_nc_cat=107&_nc_ohc=RGy4LptudhEQ7kNvgEdhSEc&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfDa4jw0DrrxmVaAWAmTdsMKk52mbZlkXgrkEX9-CEWxNg&oe=6634E9EE&_nc_sid=10d13b"
    ],
    "likes": 3556,
    "comments": 460
  },
  "_parentEntryID": "1066107462",
  "hashtags": []
}
```

### Ejemplo de extracción de datos Facebook
```
{
  "_id": {
    "$oid": "662f2444f0cd4047f0f091e0"
  },
  "type": "post de Facebook",
  "socialNetwork": "facebook",
  "content": "Cuando firmamos el acuerdo de paz en 1989, nadie dijo que quedaba prohibida la bandera del M19,  ni el M19.\n\nAl contrario, uno de los puntos más importantes fue la legalización del movimiento. Yo mismo fui congresista del M19 elegido por Cundinamarca entre 1991 y 1994.\n\nEste libro de Vera, muestra la vida de Carlos Pizarro.",
  "usernameSocialNetwork": "gustavopetrourrego",
  "dateCreated": "2024-04-28T20:58:17.000Z",
  "dateQuery": "2024-04-28 23:38:27.811723",
  "usersMentioned": [],
  "properties": {
    "postId": "991835858973985",
    "postURL": "https://www.facebook.com/gustavopetrourrego/posts/pfbid02eNBgVW5CNQye7xxQxWciq9Pw2jFSSbYAojJpHbnPCbFsJSEkbCus7AV157Ngtd87l",
    "mediaURL": [
      "https://scontent-dfw5-2.xx.fbcdn.net/v/t39.30808-6/440941586_991835798973991_7486089695585717413_n.jpg?stp=dst-jpg_p526x296&_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=ENe8wfLyxgoAb6H4gSe&_nc_ht=scontent-dfw5-2.xx&oh=00_AfDvrM3AE65Z6CIL9BlL7dWvX1Q5pj0eT3770mIL7H69gg&oe=6634DB27"
    ],
    "comments": 1066,
    "reactions": 12387,
    "shares": 1371,
    "views": null
  },
  "_parentEntryID": "100044427399729",
  "hashtags": []
}
```

## License

Este trabajo está licenciado bajo: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

****
