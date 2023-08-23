import requests
import datetime
from sqlalchemy import create_engine

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
earthquake = response.json()

#%%

# Configurar la conexión
dbname = "data-engineer-database"
user = "marcosdanielgnzlz_coderhouse"
password = input("Ingresar la contraseña: ")  #adjunto en el comentario de la entrega 
host = "data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com"
port = "5439"

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
