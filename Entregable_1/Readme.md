# Extracción y Carga de Datos de Terremotos a Redshift

En este repositorio, he compartido un script en Python que me permitió extraer datos de terremotos desde una API pública y cargarlos en una tabla en Amazon Redshift. Además, incluí el archivo que contiene el script para la creación de la tabla en formato SQL.


## Elección de la API de Terremotos

Decidí utilizar la API de terremotos de la [USGS](https://www.usgs.gov/programs/earthquake-hazards) debido a su capacidad de proporcionar datos relevantes y actualizados sobre eventos sísmicos. A pesar de que la API requiere intervalos de tiempo fijos, implementé una solución para obtener datos en tiempo real incorporando la fecha y hora del sistema en la URL de la API. Seleccioné una fecha de inicio que coincidiera con el comienzo del curso para limitar el conjunto de datos y permitir un seguimiento cronológico.

## Contenido del Repositorio

- `Entregable_1_Gonzalez_Marcos.py`: Este archivo contiene el código Python que desarrollé para extraer datos de terremotos desde la API y cargarlos en la base de datos de Redshift.
- `Entregable_1_creacion_tabla_Gonzalez_Marcos.txt`: Aquí se encuentra el script SQL que diseñé para crear la tabla en la base de datos de Redshift, donde almacenaré la información de los terremotos.


## Notas

Desarrollé este proyecto como parte de [Data Engineering Flex] en [Coderhouse]. Elegí el tema de terremotos para demostrar la capacidad del script en el manejo de datos en tiempo real, pero su estructura y enfoque son aplicables a otros conjuntos de datos.
