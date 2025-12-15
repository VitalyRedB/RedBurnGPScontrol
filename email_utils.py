import smtplib
import os
from email.message import EmailMessage

def send_confirm_email(to_email, token):
    # --- Чтение переменных окружения ---
    try:
        smtp_email = os.environ["SMTP_EMAIL"]
        smtp_password = os.environ["SMTP_PASSWORD"]
        print(f"[LOG] SMTP_EMAIL прочитан: {smtp_email}")
        print(f"[LOG] SMTP_PASSWORD прочитан: {'***' if smtp_password else 'Пустой'}")
    except KeyError as e:
        print(f"[ERROR] Не найдена переменная окружения: {e}")
        return

    # --- Формирование ссылки подтверждения ---
    confirm_link = (
        "https://redburngpscontrol.pythonanywhere.com"
        f"/confirm-email?token={token}"
    )
    print(f"[LOG] Сформирована ссылка подтверждения: {confirm_link}")

    # --- Формирование письма ---
    msg = EmailMessage()
    msg["From"] = smtp_email
    msg["To"] = to_email
    msg["Subject"] = "Подтверждение регистрации"

    msg.set_content(
        "Здравствуйте!\n\n"
        "Подтвердите регистрацию, перейдя по ссылке:\n"
        f"{confirm_link}\n\n"
        "Если вы не регистрировались — игнорируйте письмо."
    )
    print(f"[LOG] Письмо подготовлено для отправки на: {to_email}")

    # --- Отправка письма ---
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
            print(f"[LOG] Письмо успешно отправлено на: {to_email}")
    except Exception as e:
        print(f"[ERROR] Ошибка при отправке письма: {e}")

