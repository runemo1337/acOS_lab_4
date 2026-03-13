import psycopg2
from psycopg2 import OperationalError
import time

def create_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",
                port=5432,
                database="phonebook",
                user="user",
                password="password"
            )
            print("Подключились к базе данных!")
            return conn
        except OperationalError as e:
            print(f"База данных ещё не готова. Ошибка: {e}")
            print("Повторная попытка через 2 секунды...")
            time.sleep(2)

def create_contact(conn, full_name, phone_number, note):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO contacts (full_name, phone_number, note) VALUES (%s, %s, %s)",
            (full_name, phone_number, note)
        )
        conn.commit()
        print("✅ Контакт добавлен")

def get_all_contacts(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, full_name, phone_number, note FROM contacts ORDER BY id")
        return cur.fetchall()

def get_contact_by_id(conn, contact_id):
    with conn.cursor() as cur:
        cur.execute("SELECT full_name, phone_number, note FROM contacts WHERE id = %s", (contact_id,))
        return cur.fetchone()

def update_contact(conn, contact_id, full_name, phone_number, note):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE contacts SET full_name = %s, phone_number = %s, note = %s WHERE id = %s",
            (full_name, phone_number, note, contact_id)
        )
        conn.commit()
        print("✅ Контакт обновлён")

def delete_contact(conn, contact_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
        conn.commit()
        print("✅ Контакт удалён")