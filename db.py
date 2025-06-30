import sqlite3 as sl
from datetime import datetime, timedelta

#db_path = 'users.db'
db_path = "/home/abragill/db_dir/users.db"


import sqlite3

def get_user_by_username(tg_user_id: str):
    """
    Проверяет наличие пользователя в БД и возвращает его данные, если найден.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE tg_user_id = ?", (tg_user_id,))
        user = cursor.fetchone()
        
        return user

    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных:", e)
        return None

    finally:
        if conn:
            conn.close()

def user_exists(tg_user_id: str) -> bool:
    """
    Проверяет, существует ли пользователь с заданным именем в базе данных.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE tg_user_id = ? LIMIT 1", (tg_user_id,))
            return cursor.fetchone() is not None
    except:
        return False
    
def human_readable_date(date_str):
    # Преобразуем строку в объект datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    
    # Форматируем в удобочитаемый формат
    human_readable = date_obj.strftime("%d %B %Y, %H:%M:%S")
    
    return human_readable