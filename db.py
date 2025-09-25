import sqlite3
import os

# Абсолютный путь к файлу базы
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

def init_db():
    """Создаем базу и тестовые данные при первом запуске."""
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE points (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        date TEXT,
                        time TEXT,
                        lat REAL,
                        lon REAL
                    )''')

        test_data = [
            ("user1", "2025-09-19", "10:30", 55.7558, 37.6173),
            ("user2", "2025-09-19", "11:15", 59.9343, 30.3351),
            ("user3", "2025-09-18", "14:00", 56.8389, 60.6057),
            ("user4", "2025-09-18", "14:00", 46.8013, 31.1307),
        ]
        c.executemany("INSERT INTO points (user_id, date, time, lat, lon) VALUES (?, ?, ?, ?, ?)", test_data)
        conn.commit()
        conn.close()
        print("✅ База создана и заполнена тестовыми данными.")

def get_points(user_id=None, date=None, time_from=None, time_to=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = "SELECT user_id, date, time, lat, lon FROM points WHERE 1=1"
    params = []

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    if date:
        query += " AND date = ?"
        params.append(date)

    if time_from:
        query += " AND time >= ?"
        params.append(time_from)

    if time_to:
        query += " AND time <= ?"
        params.append(time_to)

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows


def add_point(user_id, date, time, lat, lon):
    """Добавляем новую точку в БД (для тестов или трекера)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO points (user_id, date, time, lat, lon) VALUES (?, ?, ?, ?, ?)",
              (user_id, date, time, lat, lon))
    conn.commit()
    conn.close()
