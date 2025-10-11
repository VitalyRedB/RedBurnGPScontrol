import sqlite3
import os

# Абсолютный путь к файлу базы
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

def get_points(user_id=None, date_from=None, date_to=None, time_from=None, time_to=None, is_active=None):
    """
    Получаем точки с возможностью фильтрации по пользователю(ям), дате, времени и активности.
    user_id может быть:
      - None => все пользователи
      - int => один пользователь
      - list[int] => несколько пользователей
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = "SELECT id, user_id, date, time, lat, lon, is_active FROM points WHERE 1=1"
    params = []

    # --- Фильтр по пользователям ---
    if user_id:
        if isinstance(user_id, list) and len(user_id) > 0:
            placeholders = ','.join(['?'] * len(user_id))
            query += f" AND user_id IN ({placeholders})"
            params.extend(user_id)
        else:
            query += " AND user_id = ?"
            params.append(user_id)

    # --- Фильтр по диапазону дат ---
    if date_from:
        query += " AND date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)

    # --- Фильтр по диапазону времени ---
    if time_from:
        query += " AND time >= ?"
        params.append(time_from)
    if time_to:
        query += " AND time <= ?"
        params.append(time_to)

    # --- Фильтр по активности ---
    if is_active is not None and is_active != "":
        active_status = int(is_active)
        query += " AND is_active = ?"
        params.append(active_status)

    query += " ORDER BY date, time"

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def get_users():
    """Возвращает список всех пользователей: [(id, name), ...]"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name FROM users ORDER BY name")
    users = c.fetchall()
    conn.close()
    return users

def add_point(user_id, date, time, lat, lon):
    """Добавляем новую точку в БД. is_active по умолчанию 1."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO points (user_id, date, time, lat, lon, is_active) VALUES (?, ?, ?, ?, ?, 1)",
        (user_id, date, time, lat, lon)
    )
    conn.commit()
    conn.close()

def execute_db_action(action, point_ids):
    """Выполняет массовые действия над точками (изменение статуса или удаление)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    placeholders = ', '.join(['?'] * len(point_ids))

    if action == "set_active":
        sql = f"UPDATE points SET is_active = 1 WHERE id IN ({placeholders})"
        c.execute(sql, point_ids)
    elif action == "set_inactive":
        sql = f"UPDATE points SET is_active = 0 WHERE id IN ({placeholders})"
        c.execute(sql, point_ids)
    elif action == "delete":
        sql = f"DELETE FROM points WHERE id IN ({placeholders})"
        c.execute(sql, point_ids)
    else:
        conn.close()
        raise ValueError(f"Неизвестное действие: {action}")

    rows_affected = c.rowcount
    conn.commit()
    conn.close()
    return rows_affected

