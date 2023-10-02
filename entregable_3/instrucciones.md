# Instrucciones para Ejecutar el Container de Docker con Airflow y el Script

## Paso 1: Construir la Imagen de Docker

Comience por construir la imagen de Docker utilizando el archivo Dockerfile proporcionado. Asegúrese de que Docker esté correctamente instalado en su sistema:
```
docker build -t nombre_de_la_imagen .
```

## Paso 2: Ejecutar el Contenedor de Docker

Ejecute el contenedor de Docker a partir de la imagen creada en el Paso 1. Asegúrese de mapear los puertos y configurar las variables de entorno adecuadas para Airflow y su script. Además, monte el archivo `.env` del repositorio en el contenedor.

```
docker run -d -p PUERTO:8080 -v ruta_del_repositorio:/root/airflow/dags --env-file ruta_del_repositorio/.env nombre_de_la_imagen
```
Tenga en cuenta que `PUERTO` representa el puerto de su elección, asegúrese de que no esté siendo utilizado por otro servicio en su sistema.


## Paso 3: Acceder a la Interfaz de Airflow

Abra un navegador web y acceda a la interfaz de Airflow en ```http://localhost:8080``` Debería encontrar el DAG 'terremotos_dag' listo para su ejecución en la interfaz de Airflow.

## Paso 4: Ejecutar el DAG

Dentro de la interfaz de Airflow, active manualmente el DAG 'terremotos_dag'. Esto iniciará la ejecución del script `terremotos_script.py` según la programación especificada en el DAG.

## Paso 5: Verificar la Ejecución

Revise el progreso y los registros de la ejecución del DAG en la interfaz de Airflow. También puede verificar cualquier salida o registro generado por el script `terremotos_script.py` para confirmar su ejecución exitosa.
