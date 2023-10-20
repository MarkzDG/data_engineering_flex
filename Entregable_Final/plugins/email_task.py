import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body, recipients, earthquake_data):
    try:
        # Configura la conexión SMTP
        smtp_server = 'smtp.example.com'
        smtp_port = 587
        smtp_username = 'your_username'
        smtp_password = 'your_password'

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Crea el mensaje de correo electrónico
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject  # Asunto personalizado

        # Cuerpo del correo personalizado con detalles de terremotos
        msg.attach(MIMEText(body, 'plain'))

        # Adjunta detalles de terremotos al cuerpo del correo
        for earthquake in earthquake_data:
            earthquake_info = f"ID: {earthquake['id']}\nLugar: {earthquake['place']}\nFecha y Hora: {earthquake['time']}\nMagnitud: {earthquake['magtype']}\nAlerta: {earthquake['alert']}\n\n"
            msg.attach(MIMEText(earthquake_info, 'plain'))

        # Envía el correo electrónico
        server.sendmail(smtp_username, recipients, msg.as_string())
        server.quit()
        print('Correo electrónico de alerta enviado con éxito.')
    except Exception as e:
        print(f'Error al enviar el correo electrónico: {str(e)}')