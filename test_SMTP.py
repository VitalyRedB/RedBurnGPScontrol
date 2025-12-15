import smtplib
from email.message import EmailMessage
import os

print("Start")

def send_confirm_email():
    #smtp_email = os.environ["SMTP_EMAIL"]
    #smtp_password = os.environ["SMTP_PASSWORD"]

    #smtp_email = os.environ.get("SMTP_EMAIL")
    #smtp_password = os.environ.get("SMTP_PASSWORD")
    token = "abc123xyz"
    to_email = 'kukoba_vitaly@ukr.net'
    smtp_email = 'redburn2025vk@gmail.com'
    smtp_password = 'wfbh vmlp uqbk isba'
    print(to_email)

    confirm_link = f"https://yourdomain.com/confirm-email?token={token}"

    msg = EmailMessage()
    msg["From"] = smtp_email
    msg["To"] = to_email
    msg["Subject"] = "Подтверждение регистрации"
    msg.set_content(
        f"Здравствуйте!\n\n"
        f"Подтвердите регистрацию, перейдя по ссылке:\n"
        f"{confirm_link}\n\n"
        f"Если вы не регистрировались — игнорируйте письмо."
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)

        print('BCE!!!')

send_confirm_email()
