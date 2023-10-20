from sqlalchemy import create_engine

def create_database(conn_string):
    try:
        engine = create_engine(conn_string)
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos!")
            connection.execute("CREATE DATABASE IF NOT EXISTS terremotos_db;")
    except Exception as e:
        print("Error al conectar a la base de datos:", e)