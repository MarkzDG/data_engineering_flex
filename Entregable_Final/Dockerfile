# Usa una imagen oficial de Apache Airflow
FROM apache/airflow:2.7.1

# Copia los archivos DAG, plugins, logs y configuración de VS Code a la ubicación correspondiente
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY logs/ /opt/airflow/logs/
COPY vscode/settings.json /home/airflow/.config/Code/User/settings.json

# Expone el puerto del servidor web de Airflow
EXPOSE 8080

# Inicia el servidor web de Airflow al ejecutar el contenedor
CMD ["webserver"]




