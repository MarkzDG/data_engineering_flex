# Guía para Ejecutar Apache Airflow con Docker

Esta guía te ayudará a ejecutar Apache Airflow en un contenedor Docker, junto con tus DAGs personalizados, plugins y configuración de Visual Studio Code. Además, te mostraremos cómo habilitar notificaciones por correo SMTP.

## Pasos para Ejecutar Apache Airflow

1. **Construye la imagen Docker:**

   Abre una terminal en la ubicación de tu Dockerfile y ejecuta el siguiente comando para construir la imagen Docker. Puedes nombrar la imagen como desees, por ejemplo, `my_airflow_image`:

   ```bash
   docker build -t my_airflow_image .

2. **Ejecuta el contenedor:**

   Utiliza Docker Compose para ejecutar el contenedor y orquestar los servicios. Asegúrate de tener un archivo `docker-compose.yml` que defina la orquestación de los servicios de Apache Airflow.

   **Nota**: Antes de ejecutar el contenedor, asegúrate de abrir el archivo `send_email_alert` en tu DAG personalizado y modificar la dirección de correo al que deseas enviar el aviso. Puedes hacerlo en la configuración de la función `send_email_alert`.

   Ejecuta el siguiente comando:

   ```bash
   docker-compose up

3. **Accede al Servidor Web de Airflow:**

   Una vez que el contenedor esté en funcionamiento, podrás acceder al servidor web de Airflow en `http://localhost:8080` en tu navegador.

Ahora podrás acceder al panel de control de Apache Airflow en tu navegador web.
