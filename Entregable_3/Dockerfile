# Utiliza la imagen oficial de Python como imagen base basada en Debian (buster)
FROM python:3.8-buster

# Instala Apache Airflow
RUN pip install apache-airflow==2.7.1

# Instala pandas y otras dependencias
RUN pip install pandas==1.0.5 requests psycopg2-binary python-dotenv sqlalchemy

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el script y el archivo .env en el contenedor
COPY terremotos_script.py .
COPY .env .

# Copia el script al directorio de DAGs de Airflow dentro del contenedor
RUN mkdir -p /root/airflow/dags/
COPY terremotos_script.py /root/airflow/dags/

# Inicializa la base de datos de Airflow
RUN airflow db init

# Define el comando para ejecutar Apache Airflow
CMD ["airflow", "scheduler"]