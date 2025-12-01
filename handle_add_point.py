from flask import request, jsonify
from db import add_point, get_last_point
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

API_TOKEN = "SECRET123"

# --- Функция для вычисления расстояния между точками (метры) ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # радиус Земли в метрах
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    return R * c

def handle_add_point():
    data = request.get_json()

    # --- Проверка токена ---
    token = data.get("token")
    if token != API_TOKEN:
        return jsonify({"status": "error", "message": "Invalid token"}), 403

    # --- Получение данных ---
    user_id = data.get("user_id")
    date = data.get("date")
    time_str = data.get("time")
    lat = data.get("lat")
    lon = data.get("lon")

    if not all([user_id, date, time_str, lat, lon]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # --- Получаем последнюю точку пользователя ---
    last_point = get_last_point(user_id)
    if last_point:
        last_dt = datetime.strptime(f"{last_point['date']} {last_point['time']}", "%Y-%m-%d %H:%M:%S")
        new_dt  = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M:%S")
        diff_seconds = abs((new_dt - last_dt).total_seconds())

        # --- Расстояние между точками ---
        dist_meters = haversine(float(lat), float(lon), float(last_point['lat']), float(last_point['lon']))

        # --- Проверка дублирования: ≤ 60 сек и ≤ 10 м ---
        if diff_seconds <= 60 and dist_meters <= 5:
            return jsonify({"status": "skipped", 
                            "message": f"Duplicate point within 1 minute and {dist_meters:.1f} m"}), 200

    # --- Добавляем точку ---
    add_point(user_id, date, time_str, lat, lon)

    return jsonify({"status": "success", "message": "Point added"})
