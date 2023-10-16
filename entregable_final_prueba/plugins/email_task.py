import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body, recipients):
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
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Envía el correo electrónico
        server.sendmail(smtp_username, recipients, msg.as_string())
        server.quit()
        print('Correo electrónico de alerta enviado con éxito.')
    except Exception as e:
        print(f'Error al enviar el correo electrónico: {str(e)}')