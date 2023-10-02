from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# Define los parámetros del DAG
default_args = {
    'owner': 'marcos',
    'start_date': datetime(2023, 1, 1),
    'schedule_interval': '@daily',  # Esto asegura que el DAG se ejecute diariamente
}

# Crea el DAG con el nombre 'terremotos_dag'
dag = DAG('terremotos_dag', default_args=default_args, description='DAG para cargar datos de terremotos')

# Define una función que ejecutará el script terremotos_script.py
def ejecutar_terremotos_script():
    subprocess.run(["python", "terremotos_script.py"])  # Reemplaza con la ruta correcta

# Define una tarea que utiliza PythonOperator para ejecutar la función
tarea_ejecucion = PythonOperator(
    task_id='tarea_ejecucion',
    python_callable=ejecutar_terremotos_script,  # Llama a la función que ejecuta el script
    dag=dag,
)
