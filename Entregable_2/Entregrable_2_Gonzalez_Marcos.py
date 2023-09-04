#%% Modulos
import requests
from datetime import datetime
from dotenv import load_dotenv, dotenv_values, find_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import concurrent.futures

#%% Configuración para el archivo .env
dotenv_path = "C:/Users/User/Desktop/Cursos/Data Engineer/Entregable 2/.env"
env = load_dotenv(find_dotenv())

#%%  Configuración para la URL de la API
# Obtener la fecha y hora actual en formato ISO8601
current_time_iso = datetime.utcnow().isoformat()

# Fecha de inicio que mantengo constante
start_time_iso = "2023-07-25T19:00:00"

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


#%% Creo una conexión a la tabla para verificar que tipo de objeto admite cada columna

conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port, options="-c client_encoding=UTF8")
cur = conn.cursor()

# Ejecutar una consulta para obtener información de las columnas de la tabla "terremotos"
cur.execute('''
    SELECT column_name, data_type, character_maximum_length
    FROM information_schema.columns
    WHERE table_name = %s;
''', ('terremotos',))

# Obtener todas las filas del conjunto de resultados
columns_info = cur.fetchall()

# Imprimir los nombres de las columnas, tipos de datos y longitud máxima (solo para character varying)
for column_info in columns_info:
    column_name, data_type, max_length = column_info
    if max_length is not None and data_type == 'character varying':
        print(f"Nombre de la Columna: {column_name}, Tipo de Datos: {data_type}, Longitud Máxima: {max_length}")
    else:
        print(f"Nombre de la Columna: {column_name}, Tipo de Datos: {data_type}")

# Cerrar el cursor y la conexión
cur.close()
conn.close()

#%% Carga de los datos

conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port, options="-c client_encoding=UTF8")
cur = conn.cursor()

# Crear un conjunto para almacenar IDs de terremotos insertados
inserted_ids = set()

def process_feature(feature):
    earthquake_id = feature['id'] or 'Info. No disponible'

    # Verificar si el ID ya ha sido insertado
    if earthquake_id not in inserted_ids:
        properties = feature['properties']
        place = properties.get('place') or 'Info. No disponible'
        time_ms = properties.get('time') or 0
        magtype = properties.get('magtype') or 'NA'
        alert = properties.get('alert') or 'NA'
        sig = properties.get('sig') or 0
        felt = properties.get('felt') or 0
        tsunami = properties.get('tsunami') or 0
        nst = properties.get('nst') or 0
        url = properties.get('url') or 'Info. No disponible'

        # Verificar si el ID ya existe en la base de datos
        cur.execute("SELECT id FROM terremotos WHERE id = %s", (earthquake_id,))
        existing_id = cur.fetchone()

        if existing_id:
            # Actualizar el registro existente si el ID ya está en la base de datos
            cur.execute("""
                UPDATE terremotos
                SET place = %s,
                    time = to_timestamp(%s),
                    magtype = %s,
                    alert = %s,
                    sig = %s,
                    felt = %s,
                    tsunami = %s,
                    nst = %s,
                    url = %s
                WHERE id = %s
            """, (place, time_ms / 1000, magtype, alert, sig, felt, tsunami, nst, url, earthquake_id))
        else:
            # Insertar un nuevo registro si el ID no está en la base de datos
            cur.execute("""
                INSERT INTO terremotos (id, place, time, magtype, alert, sig, felt, tsunami, nst, url)
                VALUES (%s, %s, to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s)
            """, (earthquake_id, place, time_ms / 1000, magtype, alert, sig, felt, tsunami, nst, url))

        # Agregar el ID al conjunto de IDs insertados
        inserted_ids.add(earthquake_id)

# Realizar la solicitud a la API
response = requests.get(api_url)

if response.status_code == 200:
    earthquake_data = response.json()
    
    # Convertir los datos JSON en un DataFrame de Pandas
    df = pd.DataFrame(earthquake_data['features'])
    
    # Procesar los datos en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_feature, df['properties'])

    conn.commit()
    print("Se extrajo y almacenó todo correctamente en la base de datos.")

    # Cerrar la conexión a la base de datos
    cur.close()
    conn.close()
else:
    print("La solicitud a la API falló.")
