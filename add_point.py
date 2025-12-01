from flask import request, jsonify
from db import add_point, get_last_point
from datetime import datetime, timedelta

API_TOKEN = "SECRET123"

def handle_add_point():
    data = request.get_json()

    # --- Проверка токена ---
    token = data.get("token")
    if token != API_TOKEN:
        return jsonify({"status": "error", "message": "Invalid token"}), 403

    # --- Получение данных ---
    user_id = data.get("user_id")
    date = data.get("date")
    time_str = data.get("time")  # строка HH:MM:SS
    lat = data.get("lat")
    lon = data.get("lon")

    if not all([user_id, date, time_str, lat, lon]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # --- Проверка на дубль в пределах 1 минуты ---
    # получаем последнюю точку пользователя
    last_point = get_last_point(user_id)
    if last_point:
        last_dt = datetime.strptime(f"{last_point['date']} {last_point['time']}", "%Y-%m-%d %H:%M:%S")
        new_dt  = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M:%S")
        diff_seconds = abs((new_dt - last_dt).total_seconds())

        # если разница <= 60 секунд и координаты совпадают
        if diff_seconds <= 60 and float(lat) == float(last_point['lat']) and float(lon) == float(last_point['lon']):
            return jsonify({"status": "skipped", "message": "Duplicate point within 1 minute"}), 200

    # --- Добавляем точку в базу ---
    add_point(user_id, date, time_str, lat, lon)

    return jsonify({"status": "success", "message": "Point added"})




