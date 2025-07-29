from db import execute_query, execute_query_with_cascade

def insertar_usuario(nombre, direccion, telefono):
    try:
        execute_query(
            "INSERT INTO CLIENTE (Nombre, Dirección, Teléfono) VALUES (%s, %s, %s)",
            (nombre, direccion, telefono)
        )
    except Exception as e:
        raise Exception(f"Error al insertar usuario: {str(e)}")

def obtener_usuarios():
    try:
        return execute_query("SELECT * FROM CLIENTE", fetch=True)
    except Exception as e:
        raise Exception(f"Error al obtener usuarios: {str(e)}")

def actualizar_usuario(cliente_id, nombre, direccion, telefono):
    try:
        execute_query(
            """UPDATE CLIENTE SET Nombre = %s, Dirección = %s, Teléfono = %s 
            WHERE Cliente_ID = %s""",
            (nombre, direccion, telefono, cliente_id)
        )
    except Exception as e:
        raise Exception(f"Error al actualizar usuario: {str(e)}")



# Para eliminar usuaio que ha estado en la tabla transacciones
def eliminar_usuario(cliente_id):
    try:
        # Primero eliminamos las transacciones relacionadas
        cascade_queries = [
            ("DELETE FROM DETALLE_TRANSACCION WHERE Transaccion_ID IN (SELECT Transaccion_ID FROM TRANSACCION WHERE Cliente_ID = %s)", (cliente_id,)),
            ("DELETE FROM TRANSACCION WHERE Cliente_ID = %s", (cliente_id,))
        ]
        
        execute_query_with_cascade(
            "DELETE FROM CLIENTE WHERE Cliente_ID = %s",
            (cliente_id,),
            cascade_queries=cascade_queries
        )
    except Exception as e:
        raise Exception(f"Error al eliminar usuario: {str(e)}")