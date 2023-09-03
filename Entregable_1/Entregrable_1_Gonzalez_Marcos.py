#%% Modulos
import requests
import datetime
import os
from dotenv import load_dotenv, dotenv_values, find_dotenv
import os
from sqlalchemy import create_engine
#%% Configuración para en .env
dotenv_path = "C:/Users/User/Desktop/Cursos/Data Engineer/Entregable 2/.env"
env = load_dotenv(find_dotenv())

#%% 

# Obtener la fecha y hora actual en formato ISO8601
current_time_iso = datetime.datetime.utcnow().isoformat()

# Fecha de inicio que mantengo constante
start_time_iso = "2023-07-25T19:00:00" #El inicio del curso

# Construir la URL de la API con los parámetros actualizados
base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
starttime_param = f"starttime={start_time_iso}"
endtime_param = f"endtime={current_time_iso}"
api_url = f"{base_url}&{endtime_param}&{starttime_param}"

#%% 

# Consulta a la API
response = requests.get(api_url)
if response.status_code == 200:  # Verifica si la solicitud fue exitosa
    earthquake_data = response.json()
    features = earthquake_data.get('features', [])

    for feature in features:
        properties = feature.get('properties', {})
        mag = properties.get('mag')
        place = properties.get('place')
        time = properties.get('time')

        print(f"Mag: {mag}, Place: {place}, Time: {time}")
else:
    print("La solicitud a la API falló.")

#%%

# Configurar la conexión
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

# %%
