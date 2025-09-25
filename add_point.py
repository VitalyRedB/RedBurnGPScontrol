from flask import request, jsonify
from db import add_point

# глобальный токен (потом можно сделать персональные)
API_TOKEN = "MY_SECRET_TOKEN"

def handle_add_point():
    data = request.get_json()

    # Проверка токена
    token = data.get("token")
    if token != API_TOKEN:
        return jsonify({"status": "error", "message": "Invalid token"}), 403

    # Получение данных
    user_id = data.get("user_id")
    date = data.get("date")
    time = data.get("time")
    lat = data.get("lat")
    lon = data.get("lon")

    # Проверка, что все данные есть
    if not all([user_id, date, time, lat, lon]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # Добавляем в базу
    add_point(user_id, date, time, lat, lon)

    return jsonify({"status": "success", "message": "Point added"})



