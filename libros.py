from db import execute_query

def insertar_libro(titulo, autor, anio):
    try:
        execute_query(
            "INSERT INTO LIBRO (Título, Autor, Año_Publicación) VALUES (%s, %s, %s)",
            (titulo, autor, anio)
        )
    except Exception as e:
        raise Exception(f"Error al insertar libro: {str(e)}")

def obtener_libros():
    try:
        return execute_query("SELECT * FROM LIBRO", fetch=True)
    except Exception as e:
        raise Exception(f"Error al obtener libros: {str(e)}")

def actualizar_libro(libro_id, titulo, autor, anio):
    try:
        execute_query(
            """UPDATE LIBRO SET Título = %s, Autor = %s, Año_Publicación = %s 
            WHERE Libro_ID = %s""",
            (titulo, autor, anio, libro_id)
        )
    except Exception as e:
        raise Exception(f"Error al actualizar libro: {str(e)}")

def eliminar_libro(libro_id):
    try:
        execute_query(
            "DELETE FROM LIBRO WHERE Libro_ID = %s",
            (libro_id,)
        )
    except Exception as e:
        raise Exception(f"Error al eliminar libro: {str(e)}")

def verificar_disponibilidad(libro_id):
    try:
        resultado = execute_query(
            """SELECT COUNT(*) FROM DETALLE_TRANSACCION dt
            JOIN TRANSACCION t ON dt.Transaccion_ID = t.Transaccion_ID
            WHERE dt.Libro_ID = %s AND t.Tipo = 'PRÉSTAMO' 
            AND dt.Fecha_Devolucion IS NULL""",
            (libro_id,), fetch=True
        )
        return resultado[0][0] == 0
    except Exception as e:
        raise Exception(f"Error al verificar disponibilidad: {str(e)}")