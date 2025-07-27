from db import execute_query
from datetime import date

def registrar_prestamo(cliente_id, libro_id):
    try:
        # Primero verificamos que el libro esté disponible
        disponible = execute_query(
            """SELECT COUNT(*) FROM DETALLE_TRANSACCION dt
            JOIN TRANSACCION t ON dt.Transaccion_ID = t.Transaccion_ID
            WHERE dt.Libro_ID = %s AND t.Tipo = 'PRÉSTAMO' 
            AND dt.Fecha_Devolucion IS NULL""",
            (libro_id,), fetch=True
        )
        
        if disponible[0][0] > 0:
            raise Exception("El libro no está disponible para préstamo")

        # Registramos la transacción
        transaccion_id = execute_query(
            """INSERT INTO TRANSACCION (Fecha, Tipo, Cliente_ID) 
            VALUES (%s, %s, %s) RETURNING Transaccion_ID""",
            (date.today(), 'PRÉSTAMO', cliente_id), fetch=True
        )[0][0]

        # Registramos el detalle
        execute_query(
            """INSERT INTO DETALLE_TRANSACCION 
            (Transaccion_ID, Libro_ID) VALUES (%s, %s)""",
            (transaccion_id, libro_id)
        )
    except Exception as e:
        raise Exception(f"Error al registrar préstamo: {str(e)}")

def registrar_devolucion(cliente_id, libro_id):
    try:
        # Verificamos que exista un préstamo activo
        prestamo = execute_query(
            """SELECT dt.Detalle_ID FROM DETALLE_TRANSACCION dt
            JOIN TRANSACCION t ON dt.Transaccion_ID = t.Transaccion_ID
            WHERE t.Cliente_ID = %s AND dt.Libro_ID = %s 
            AND t.Tipo = 'PRÉSTAMO' AND dt.Fecha_Devolucion IS NULL""",
            (cliente_id, libro_id), fetch=True
        )
        
        if not prestamo:
            raise Exception("No existe un préstamo activo para este libro y cliente")

        # Actualizamos la fecha de devolución
        execute_query(
            """UPDATE DETALLE_TRANSACCION 
            SET Fecha_Devolucion = %s 
            WHERE Detalle_ID = %s""",
            (date.today(), prestamo[0][0])
        )
    except Exception as e:
        raise Exception(f"Error al registrar devolución: {str(e)}")

def obtener_estatus_libros():
    try:
        return execute_query(
            """SELECT l.Libro_ID, 
            CASE WHEN EXISTS (
                SELECT 1 FROM DETALLE_TRANSACCION dt
                JOIN TRANSACCION t ON dt.Transaccion_ID = t.Transaccion_ID
                WHERE dt.Libro_ID = l.Libro_ID 
                AND t.Tipo = 'PRÉSTAMO' 
                AND dt.Fecha_Devolucion IS NULL
            ) THEN FALSE ELSE TRUE END AS disponible
            FROM LIBRO l""",
            fetch=True
        )
    except Exception as e:
        raise Exception(f"Error al obtener estatus de libros: {str(e)}")