import smtplib
from email.message import EmailMessage
import os

def send_email(to, subject, body):
    html_body = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <style>
            body {{
                font-family: sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #fff;
                padding: 2rem;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header h1 {{
                color: #333;
                margin: 0;
            }}
            .content {{
                margin-bottom: 20px;
            }}
            .button {{
                font-size: 16px;
                font-weight: 700;
                color: #df93d2;
                background-color: #2B3044;
                border: none;
                outline: none;
                cursor: pointer;
                padding: 12px 24px;
                line-height: 24px;
                border-radius: 9px;
                box-shadow: 0px 1px 2px #2B3044,
                    0px 4px 16px #2B3044;
                display: flex;
                align-self: center;
                text-decoration: none;
                text-align: center;
            }}
            .button:hover {{
                transition: 0.3s;
                transform: scale(0.93);
            }}
            @media (max-width: 480px) {{
                .container {{
                    padding: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Restablecer Contraseña</h1>
            </div>
            <div class="content">
                <p>Hemos recibido una solicitud para restablecer tu contraseña. Si no has sido tú, ignora este correo electrónico.</p>
                <p>Para restablecer tu contraseña, haz clic en el siguiente botón:</p>
                <a href="{body}" class="button">Restablecer Contraseña</a>
                <p>Este enlace expirará en 24 horas.</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = to
    msg.set_content(html_body, subtype='html')

    print(f"Sending email... {os.getenv('EMAIL_FROM')}")
    try:
        with smtplib.SMTP(os.getenv("EMAIL_HOST"), 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
            smtp.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")