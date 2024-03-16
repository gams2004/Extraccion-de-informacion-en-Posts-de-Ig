# Extracción de información en Posts de Instagram
Proyecto en Python que extraerá texto de los posts de un perfil de Instagram cada 24 horas utilizando la librería Profile Scraper. Además, realiza un análisis de sentimientos con la librería PySentimiento.

Librerías utilizadas para el proyecto:
- schedule = `pip install schedule`
- time = `pip install time`
- apify = `pip install apify-client`
- pysentimiento = `pip install pysentimiento` 
- wandb (Dependencia de pysentimiento) = `pip install wandb`

Es importante contar con las últimas versiones de Python y PIP para correr el proyecto sin problemas.

Para ejecutarlo basta con llamar a la función `obtener_sentimientos_instagram` y pasarle el usuario a buscar. 

*Importante*: En la línea `client = ApifyClient("<TOKEN API>")` es necesario ingresar tu token de apify para poder ejecutar el código

## Decisiones de diseño

La función `obtener_sentimientos_instagram` recibe como parámetro un nombre de usuario para el cuál buscará la descripción de los primeros 10 posts (La cantidad de posts a revisar se puede mofificar) y devolverá el análisis de sentimiento y los captions de los posts. Para esto se utilizó una estructura lambda que permite desenlazar la función de un identificador, abreviando su escritura. 

## Salida de datos

La función devolverá un diccionario con el análisis y las descripciones, los análisis estarán ligados al identificador `"analisis"` y las descripciones al identificador `"resultado"`. Esto debido a la naturaleza de las funciones lambda, que intenta simplificar la escritura de funciones y nos invita a utilizar estas estructuras de datos. 
Un ejemplo de salida, para un análisis de los 10 posts de la universidad Javeriana sería:

Análisis:

```
{'resultado': [AnalyzerOutput(output=NEU, probas={NEU: 0.557, POS: 0.357, NEG: 0.086}), AnalyzerOutput(output=NEU, probas={NEU: 0.560, POS: 0.343, NEG: 0.097}), AnalyzerOutput(output=NEU, probas={NEU: 0.601, POS: 0.355, NEG: 0.044}), AnalyzerOutput(output=POS, probas={POS: 0.555, NEU: 0.400, NEG: 0.045}), AnalyzerOutput(output=NEU, probas={NEU: 0.762, POS: 0.140, NEG: 0.098}), AnalyzerOutput(output=NEU, probas={NEU: 0.729, POS: 0.219, NEG: 0.051}), AnalyzerOutput(output=NEU, probas={NEU: 0.800, POS: 0.122, NEG: 0.078}), AnalyzerOutput(output=NEU, probas={NEU: 0.710, POS: 0.249, NEG: 0.042}), AnalyzerOutput(output=POS, probas={POS: 0.517, NEU: 0.442, NEG: 0.042}), AnalyzerOutput(output=NEU, probas={NEU: 0.628, POS: 0.306, NEG: 0.066})]
```

Captions:

```
'Captions': ['#LaJaverianaTeCuenta que estamos comprometidos con el futuro de nuestros estudiantes, por eso te contamos las diferentes alternativas de financiación y convenios que tenemos para ti.\n\n✅ Corto, mediano y largo plazo\n✅ Líneas de crédito con el ICETEX\n✅ Convenios\n✅ Entre otros\n\nConoce más en el link de nuestra biografía.', '#PostalJaveriana 💛💙 ¡Conmemoramos el #DíaDeLaMujer en nuestro campus! Te compartimos algunas fotografías del #8M en la Javeriana, un día en el que el diálogo, el reconocimiento y el acompañamiento fueron protagonistas.\n\nCada imagen refleja el amor de las #MujeresJaverianas 💜', 'Te compartimos las 3️⃣ #NoticiasJaverianas más importantes de esta semana, contadas en un minuto por nuestros profesores, estudiantes y administrativos.\n\nSi quieres conocer todas las noticias, visita: www.javeriana.edu.co', '#LaJaverianaTeCuenta cuáles son las becas que te ofrecemos en la Universidad, para neojaverianos y para estudiantes de pregado y de posgrado, además de créditos condonables de apoyo a especializaciones, maestrías y doctorados. \n\nTe invitamos a conocer cada una de estas opciones en el siguiente video y en el link de nuestra\xa0biografía.', '#LaJaverianaTeCuenta | Estos son algunos de los descuentos que ofrecemos para la financiación de tu matrícula:\n \n✅ Egresado Javeriano \n✅ Hermanos Javerianos\n✅ Familias Javerianas\n✅ Hijos de empleados\n✅ Entre otros\n\nConoce más información en el link de nuestra biografía.', '#RegálemeUnMinuto para conocer la conexión que existe entre el calentamiento global y la calidad del sueño, contada por Alain Riveros-Rivera, profesor de @medicina.puj, en el marco del #DíaMundialDelSueño, que se celebra este viernes 15 de marzo.'...
```

## License

Este trabajo está licenciado bajo: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

****
