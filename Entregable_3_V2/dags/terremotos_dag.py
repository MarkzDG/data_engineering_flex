from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv, find_dotenv
import requests
from sqlalchemy import create_engine
import psycopg2
import pandas as pd

# Define los parámetros predeterminados del DAG
default_args = {
    'owner': 'marcos',
    'start_date': datetime(2023, 1, 1),
    'schedule_interval': '@daily',
    'retry_delay': timedelta(minutes=5),  # Tiempo de espera entre reintentos
    'retries': 5,  # Número máximo de reintentos en caso de fallo
}

# Define las credenciales de la base de datos
dotenv_path = ".env"
env = load_dotenv(find_dotenv())

dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')

conn_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Task 1: Creación de la Base de Datos (si no existe)
def task1():
    try:
        engine = create_engine(conn_string)
        
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos!")
            connection.execute("CREATE DATABASE IF NOT EXISTS terremotos_db;")
    except Exception as e:
        print("Error al conectar a la base de datos:", e)

# Task 2: Obtener datos de la API de terremotos y guardar en una tabla en la base de datos
def task2():
    try:
        # Realiza la solicitud a la API y obtiene los datos en formato JSON
        current_time_iso = datetime.utcnow().isoformat()
        start_time_iso = "2023-09-01T19:00:00"
        base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
        starttime_param = f"starttime={start_time_iso}"
        endtime_param = f"endtime={current_time_iso}"
        api_url = f"{base_url}&{endtime_param}&{starttime_param}"
        response = requests.get(api_url)

        if response.status_code == 200:
            earthquake_data = response.json()
            features = earthquake_data.get('features', [])

            # Establece la conexión a la base de datos
            conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port,
                                    options="-c client_encoding=UTF8")
            cur = conn.cursor()

            # Obtiene los IDs existentes en la base de datos
            cur.execute("SELECT id FROM terremotos;")
            existing_ids = set([row[0] for row in cur.fetchall()])

            # Itera a través de los datos de la API y carga en la base de datos
            for feature in features:
                earthquake_id = feature.get('id') or 'Info. No disponible'

                # En caso de no existir el ID, carga los demás datos
                if earthquake_id not in existing_ids:
                    properties = feature.get('properties', {})
                    place = properties.get('place') or 'Info. No disponible'
                    time_ms = properties.get('time') or 0
                    time_dt = datetime.utcfromtimestamp(time_ms / 1000)
                    formatted_time = time_dt.strftime('%Y-%m-%d %H:%M:%S')
                    magtype = properties.get('magtype') or 'NA'
                    alert = properties.get('alert') or 'NA'
                    sig = properties.get('sig') or 0
                    felt = properties.get('felt') or 0
                    tsunami = properties.get('tsunami') or 0
                    nst = properties.get('nst') or 0
                    url = properties.get('url') or 'Info. No disponible'

                    # Inserta el registro en la base de datos si no existe
                    cur.execute("""
                        INSERT INTO terremotos (id, place, time, magtype, alert, sig, felt, tsunami, nst, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (earthquake_id, place, formatted_time, magtype, alert, sig, felt, tsunami, nst, url))

                    # Agrega el ID al conjunto de IDs insertados
                    existing_ids.add(earthquake_id)

            conn.commit()
            print("Se extrajo y almacenó todo correctamente en la base de datos.")

            # Cierra la conexión a la base de datos
            cur.close()
            conn.close()
        else:
            print("La solicitud a la API falló.")
    except Exception as e:
        print("Error al obtener datos de la API o cargarlos en la base de datos:", str(e))

# Crea el DAG
dag = DAG('terremotos_dag', default_args=default_args, description='DAG para cargar datos de terremotos')

# Define las tareas utilizando PythonOperator
task1 = PythonOperator(
    task_id='task1',
    python_callable=task1,
    dag=dag,
)

task2 = PythonOperator(
    task_id='task2',
    python_callable=task2,
    dag=dag,
)

# Define la secuencia de tareas: task1 -> task2
task1 >> task2
