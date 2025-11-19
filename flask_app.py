#/home/RedBurnGPScontrol/mysite/flask_app.py

from flask import Flask, jsonify, render_template, request
from db import get_points, get_users, execute_db_action
from add_point import handle_add_point
from db import DB_NAME
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    """Главная страница: карта GPS-точек."""
    return render_template("map.html")

@app.route("/new/")
def index_new():
    """Новая карта для новых таблиц (points_new, trackers, users)."""
    return render_template("map_new.html")



@app.route("/api/points")
def api_points():
    """
    API для получения GPS-точек с фильтрацией по user_id (строка),
    диапазону дат/времени и активности.
    """
    user_ids = request.args.getlist("user_id")  # например ['user1', 'user3']
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    time_from = request.args.get("time_from")
    time_to = request.args.get("time_to")
    is_active = request.args.get("is_active")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = """
        SELECT id, user_id, date, time, lat, lon, is_active
        FROM points
        WHERE 1=1
    """
    params = []

    # --- Фильтр по пользователям (текстовый) ---
    if user_ids:
        placeholders = ','.join(['?'] * len(user_ids))
        query += f" AND user_id IN ({placeholders})"
        params.extend(user_ids)

    # --- Фильтр по датам ---
    if date_from:
        query += " AND date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)

    # --- Фильтр по времени ---
    if time_from:
        query += " AND time >= ?"
        params.append(time_from)
    if time_to:
        query += " AND time <= ?"
        params.append(time_to)

    # --- Фильтр по активности ---
    if is_active is not None and is_active != "":
        query += " AND is_active = ?"
        params.append(int(is_active))

    query += " ORDER BY date, time"

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    return jsonify([
        {"id": p[0], "user_id": p[1], "date": p[2], "time": p[3],
         "lat": p[4], "lon": p[5], "is_active": p[6]}
        for p in rows
    ])


@app.route("/api/points_new")
def api_points_new():
    """
    API для получения GPS-точек из points_new
    для выбранного пользователя.
    """
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify([])  # если пользователь не указан, возвращаем пустой список

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Получаем все точки пользователя
    cur.execute("""
        SELECT id, tracker_id, tracker_uid, tracker_name, date, time, lat, lon, speed, altitude, direction, is_active
        FROM points_new
        WHERE user_id = ?
        ORDER BY date, time
    """, (user_id,))

    points = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(points)



@app.route("/api/trackers")
def api_trackers():
    """Возвращает трекеры для выбранного пользователя"""
    user_id = request.args.get("user_id")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if user_id:
        c.execute("SELECT id, tracker_name, user_id FROM trackers WHERE user_id = ?", (user_id,))
    else:
        c.execute("SELECT id, tracker_name, user_id FROM trackers")
    trackers = [{"id": row[0], "tracker_name": row[1], "user_id": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(trackers)

@app.route("/api/users_new")
def api_users_new():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT id, username FROM users ORDER BY username")
    users = [dict(row) for row in cur.fetchall()]

    conn.close()
    return jsonify(users)




@app.route("/api/users")
def api_users():
    """API для получения списка всех пользователей для фильтра."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT DISTINCT user_id FROM points ORDER BY user_id")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify(users)


@app.route("/show_points")
def show_points():
    """Отображение всех точек без фильтров."""
    points = get_points(
        user_id=None,
        date_from=None,
        date_to=None,
        time_from=None,
        time_to=None,
        is_active=None
    )
    return render_template("show_points.html", points=points)

@app.route("/api/add_point", methods=["POST"])
def api_add_point():
    """Роут для добавления новой точки (от трекера)."""
    return handle_add_point()

@app.route("/api/execute_action", methods=["POST"])
def api_execute_action():
    """API для массовых действий над точками."""
    try:
        data = request.get_json()
        action = data.get("action")
        point_ids = data.get("point_ids")

        if not action or not point_ids:
            return jsonify({"status": "error", "message": "Не указано действие или ID точек"}), 400

        result = execute_db_action(action, point_ids)

        return jsonify({"status": "success", "action": action, "count": result})
    except Exception as e:
        print(f"Ошибка при выполнении действия: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500




# Новый маршрут 25_10_2025 - удаление ТТ и замена статуса
@app.route('/delete_points', methods=['POST'])
def delete_points():
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'success': False, 'error': 'No IDs provided'})
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.executemany("DELETE FROM points WHERE id = ?", [(i,) for i in ids])
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print("Error in /delete_points:", e)
        return jsonify({'success': False, 'error': str(e)})

# Новый маршрут 25_10_2025 - удаление ТТ и замена статуса
@app.route('/change_status', methods=['POST'])
def change_status():
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'success': False, 'error': 'No IDs provided'})

    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        placeholders = ','.join(['?'] * len(ids))
        cur.execute(f"""
            UPDATE points
            SET is_active = CASE WHEN is_active = 1 THEN 0 ELSE 1 END
            WHERE id IN ({placeholders})
        """, ids)

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True})

    except Exception as e:
        print("Error in /change_status:", e)
        return jsonify({'success': False, 'error': str(e)})


@app.route("/set_user")
def set_user():
    uid = request.args.get("uid")
    resp = jsonify({"status": "ok"})
    resp.set_cookie("uid", uid, max_age=60*60*24*365)
    return resp

@app.route("/whoami")
def whoami():
    uid = request.cookies.get("uid")
    if not uid:
        return jsonify({"user": None})

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE id=?", (uid,))
    row = cur.fetchone()
    conn.close()

    return jsonify({"user": dict(row) if row else None})



if __name__ == "__main__":
    app.run(debug=True)




