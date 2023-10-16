import os
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from api_task import get_earthquake_data
from database_task import create_database
from email_task import send_email_alert
from export_task import export_data_to_xcom

# Define las credenciales de la base de datos
dotenv_path = ".env"
env = load_dotenv(find_dotenv())

dbname = os.getenv('DBNAME')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')

conn_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Define los parámetros predeterminados del DAG
default_args = {
    'owner': 'marcos',
    'start_date': datetime(2023, 1, 1),
    'schedule_interval': '@daily',
    'retry_delay': timedelta(minutes=5),  # Tiempo de espera entre reintentos
    'retries': 5,  # Número máximo de reintentos en caso de fallo
}

# Crear un DAG
dag = DAG('terremotos_dag', default_args=default_args, description='DAG para cargar datos de terremotos')

def decide_email_or_export(**kwargs):
    ti = kwargs['ti']
    exported_data = ti.xcom_pull(task_ids='export_data_task')

    # Verifica si la variable 'nst' en los datos exportados es mayor que 10
    nst_value = exported_data[0]['nst'] if exported_data else None

    if nst_value is not None and nst_value > 10:
        return 'send_email_alert'  # Si nst > 10, enviar correo
    return 'export_data_to_xcom'  # En cualquier otro caso, exportar tabla

default_args = {
    'owner': 'marcos',
    'start_date': datetime(2023, 1, 1),
    'schedule_interval': '@daily',
    'retry_delay': timedelta(minutes=5),
    'retries': 5,
}

with DAG('terremotos_dag', default_args=default_args, description='DAG para cargar datos de terremotos') as dag:
    task1 = PythonOperator(
        task_id='task1',
        python_callable=create_database,
        op_args=[conn_string],
    )

    task2 = PythonOperator(
        task_id='task2',
        python_callable=get_earthquake_data,
        op_args=[conn_string],
    )

    task3 = PythonOperator(
        task_id='send_email_alert',
        python_callable=send_email_alert,
        op_args=['Asunto del Correo', 'Cuerpo del Correo', ['correo_destinatario@example.com']],
    )

    task4 = PythonOperator(
        task_id='export_data_to_xcom',
        python_callable=export_data_to_xcom,
        op_args=['your_postgres_connection', 'SELECT * FROM terremotos LIMIT 10'],
    )

    decide_email_or_export_task = PythonOperator(
        task_id='decide_email_or_export',
        python_callable=decide_email_or_export,
        provide_context=True,
    )

    decide_email_or_export_task >> task3
    decide_email_or_export_task >> task4

    task1 >> task2 >> decide_email_or_export_task