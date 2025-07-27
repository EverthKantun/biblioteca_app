# db.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print("Error de conexión con la base de datos:", e)
        return None

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    result = None
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                conn.commit()
        except Exception as e:
            print("Error al ejecutar consulta:", e)
            raise e  # Re-lanzamos la excepción para manejarla en las capas superiores
        finally:
            conn.close()
    return result