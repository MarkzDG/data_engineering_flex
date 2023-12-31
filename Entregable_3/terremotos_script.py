#%% 
import requests
from datetime import datetime
from dotenv import load_dotenv, dotenv_values, find_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
#%% Configuración para el archivo .env
dotenv_path = ".env"
env = load_dotenv(find_dotenv())

#%%  Configuración para la URL de la API
# Obtener la fecha y hora actual en formato ISO8601
current_time_iso = datetime.utcnow().isoformat()

# Fecha de inicio que mantengo constante
start_time_iso = "2023-09-01T19:00:00" #El inicio del curso

# Construir la URL de la API con los parámetros actualizados
base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
starttime_param = f"starttime={start_time_iso}"
endtime_param = f"endtime={current_time_iso}"
api_url = f"{base_url}&{endtime_param}&{starttime_param}"

#%% Configurar la conexión a la base de datos

dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')

# Crea la cadena de conexión
conn_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Crea el motor de conexión
engine = create_engine(conn_string)

# Anade un mensaje de como fue la conexión
try:
    with engine.connect() as connection:
        # Si no ocurre una excepción, la conexión fue exitosa
        print("Conexión exitosa a la base de datos!")

        # Si algo sale mal, muestra un mensaje de error junto con la descripción de la excepción
except Exception as e:
    print("Error al conectar a la base de datos:", e)

#%% Cargar archivos a la base de datos verificando que no hayan filas duplicadas
inserted_ids = set()

response = requests.get(api_url)

if response.status_code == 200:
    earthquake_data = response.json()
    features = earthquake_data.get('features', [])

    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port, options="-c client_encoding=UTF8")
    cur = conn.cursor()

    # Obtener los IDs existentes en la base de datos
    cur.execute("SELECT id FROM terremotos;")
    existing_ids = set([row[0] for row in cur.fetchall()])

    # Iterar a través de los datos de la API
    for feature in features:
        earthquake_id = feature.get('id') or 'Info. No disponible'

        # En caso de no existir el id carga entonces los demas datos
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

            # Insertar el registro en la base de datos si no existe
            cur.execute("""
                INSERT INTO terremotos (id, place, time, magtype, alert, sig, felt, tsunami, nst, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (earthquake_id, place, formatted_time, magtype, alert, sig, felt, tsunami, nst, url))

            # Agregar el ID al conjunto de IDs insertados
            inserted_ids.add(earthquake_id)

    conn.commit()
    print("Se extrajo y almacenó todo correctamente en la base de datos.")

    # Cerrar la conexión a la base de datos
    cur.close()
    conn.close()
else:
    print("La solicitud a la API falló.")
# %%
