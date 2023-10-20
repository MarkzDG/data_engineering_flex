# Guía para Ejecutar Apache Airflow con Docker

Esta guía te ayudará a ejecutar Apache Airflow en un contenedor Docker, junto con tus DAGs personalizados, plugins y configuración de Visual Studio Code. Además, te mostraremos cómo habilitar notificaciones por correo SMTP.

## Pasos para Ejecutar Apache Airflow

   **Nota**: Antes de ejecutar el contenedor, asegúrate de abrir el archivo `email_task.py` (dentro de la carpeta plugins) y modificar la dirección de correo al que deseas enviar el aviso.

1. **Construye la imagen Docker:**

   Abrir una terminal en la ubicación de tu Dockerfile y ejecutar el siguiente comando para construir la imagen Docker. Se puede nombrar la imagen como desees, por ejemplo, `my_airflow_image`:

   ```bash
   docker build -t my_airflow_image .

2. **Ejecutar el contenedor:**

   Ejecutar el siguiente comando en la terminal:

   ```bash
   docker-compose up

3. **Accede al Servidor Web de Airflow:**

   Una vez que el contenedor esté en funcionamiento, podrás acceder al servidor web de Airflow en `http://localhost:8080` en tu navegador.

Ahora podrás acceder al panel de control de Apache Airflow en tu navegador web.

# Sobre el Proyecto

El proyecto del DAG "terremotos_dag" es una iniciativa que busca automatizar la gestión de datos relacionados con terremotos. A través de la plataforma Apache Airflow, hemos diseñado un flujo de trabajo eficiente para abordar las siguientes tareas:

1. **Creación de Base de Datos**: Configuración y creación de una base de datos para el almacenamiento de datos de terremotos.

2. **Obtención de Datos**: Descarga y actualización regular de datos de terremotos desde fuentes externas.

3. **Exportación de Datos**: Extracción de información relevante de la base de datos y su exportación para su análisis.

4. **Alertas por Correo Electrónico**: Envío de notificaciones por correo electrónico en caso de condiciones específicas en los datos.

## Objetivos

- Automatizar procesos manuales relacionados con la gestión de datos de terremotos.
- Garantizar la disponibilidad de datos actualizados y su almacenamiento seguro.
- Facilitar el análisis de datos a través de la exportación de información relevante.
- Notificar al equipo en caso de situaciones críticas.

## Pasos Clave

1. **Configuración Inicial**: Se establecieron las credenciales de la base de datos y se exploraron las fuentes de datos disponibles.

2. **Creación del DAG**: Se configuró el DAG "terremotos_dag" con parámetros como el propietario y la programación.

3. **Definición de Tareas**: Se crearon tareas para gestionar la creación de la base de datos, la obtención de datos de terremotos, la exportación de datos y el envío de correos electrónicos de alerta.

4. **Relaciones de Dependencia**: Se definió la secuencia de ejecución de las tareas, asegurando que ciertas tareas dependieran del éxito de otras.

5. **Ejecución y Monitoreo**: El DAG se lanzó en el entorno de Apache Airflow, y su ejecución y estado se monitorearon a través del panel de control.

## Resultados

- Automatización de tareas previamente manuales, lo que ha reducido la carga de trabajo.
- Datos de terremotos disponibles y actualizados en la base de datos.
- Facilitación del análisis de datos a través de la exportación de información relevante.
- Notificaciones por correo electrónico en caso de situaciones críticas.

## Lecciones Aprendidas

- La automatización ahorra tiempo y recursos.
- La planificación adecuada de las relaciones de dependencia es fundamental.
- Apache Airflow es una herramienta poderosa para gestionar flujos de trabajo.

## Futuras Expansiones

El proyecto "terremotos_dag" sienta las bases para futuras expansiones. Podríamos explorar la optimización de tareas, la integración con más fuentes de datos y la expansión de la plataforma para abordar otros tipos de datos.
