from datetime import datetime
import requests
import psycopg2

def get_earthquake_data(conn_string):
    try:
        # Obtener datos de la API y almacenarlos en la base de datos
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

            # Establece la conexión a la base de datos usando el conn_string
            conn = psycopg2.connect(conn_string)
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