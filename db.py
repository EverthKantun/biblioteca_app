# Usaremos psycopg2 para el manejo de la bd
import psycopg2
import os
#Aquí importamos el .env, si alguien lo quiere usar ahí se asignan las variables de su bd
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

# para eliminar un usuario que ha estado en la tabla de transacciones
def execute_query_with_cascade(query, params=None, fetch=False, cascade_queries=None):
    conn = get_connection()
    result = None
    if conn:
        try:
            with conn.cursor() as cursor:
                if cascade_queries:
                    for cascade_query, cascade_params in cascade_queries:
                        cursor.execute(cascade_query, cascade_params)
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                conn.commit()
        except Exception as e:
            print("Error al ejecutar consulta en cascada:", e)
            raise e
        finally:
            conn.close()
    return result