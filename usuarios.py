from db import execute_query

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

def eliminar_usuario(cliente_id):
    try:
        execute_query(
            "DELETE FROM CLIENTE WHERE Cliente_ID = %s",
            (cliente_id,)
        )
    except Exception as e:
        raise Exception(f"Error al eliminar usuario: {str(e)}")