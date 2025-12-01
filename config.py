# config.py
# DB_NAME = "database.db"

import os

# Абсолютный путь к файлу базы
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")
