# Instrucciones para Ejecutar el DAG de Airflow con Docker Compose

## Paso 1: Ejecución con Docker Compose

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2. Abre una terminal en la ubicación donde se encuentra tu archivo `docker-compose.yml`.
3. Ejecuta el siguiente comando para iniciar Airflow y el DAG:
`
docker-compose up
`

Esto iniciará Apache Airflow junto con tu DAG terremotos_dag.

## Paso 2: Acceso a la Interfaz de Airflow

Abre un navegador web y accede a la interfaz de Airflow en http://localhost:8080.

**Observación:** El puerto puede variar dependiendo de tu configuración. Asegúrate de verificar el puerto correcto. Para ello se puede ver en la terminal mediante `docker-compose ps`

Deberías encontrar el DAG terremotos_dag listo para su ejecución en la interfaz de Airflow.

## Paso 3: Ejecución del DAG

Dentro de la interfaz de Airflow, activa manualmente el DAG terremotos_dag.

Esto iniciará la ejecución del script según la programación especificada en el DAG.

Monitorea el progreso y los registros de la ejecución en la interfaz de Airflow.

Con esto se ha configurado y ejecutado el DAG de Airflow con Docker Compose.
