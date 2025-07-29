from db import execute_query
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def obtener_estadisticas(con_graficas=False, master=None):
    try:
        # Libros más prestados (top 5)
        libros_mas_prestados = execute_query(
            """SELECT l.Libro_ID, l.Título, COUNT(dt.Detalle_ID) as prestamos 
            FROM LIBRO l
            JOIN DETALLE_TRANSACCION dt ON l.Libro_ID = dt.Libro_ID
            JOIN TRANSACCION t ON dt.Transaccion_ID = t.Transaccion_ID
            WHERE t.Tipo = 'PRÉSTAMO'
            GROUP BY l.Libro_ID, l.Título
            ORDER BY prestamos DESC
            LIMIT 5""",
            fetch=True
        )
        
        # Usuarios más activos (top 5)
        usuarios_activos = execute_query(
            """SELECT c.Cliente_ID, c.Nombre, COUNT(t.Transaccion_ID) as transacciones
            FROM CLIENTE c
            JOIN TRANSACCION t ON c.Cliente_ID = t.Cliente_ID
            GROUP BY c.Cliente_ID, c.Nombre
            ORDER BY transacciones DESC
            LIMIT 5""",
            fetch=True
        )
        
        # Porcentaje de disponibilidad
        disponibilidad = execute_query(
            """SELECT 
                (SELECT COUNT(*) FROM LIBRO WHERE Libro_ID NOT IN (
                    SELECT DISTINCT dt.Libro_ID FROM DETALLE_TRANSACCION dt
                    JOIN TRANSACCION t ON dt.Transaccion_ID = t.Transaccion_ID
                    WHERE t.Tipo = 'PRÉSTAMO' AND dt.Fecha_Devolucion IS NULL
                )) * 100.0 / NULLIF(COUNT(*), 0) as porcentaje_disponible
            FROM LIBRO""",
            fetch=True
        )
        
        resultado = {
            'libros_mas_prestados': libros_mas_prestados or [],
            'usuarios_activos': usuarios_activos or [],
            'porcentaje_disponible': round(disponibilidad[0][0], 2) if disponibilidad and disponibilidad[0][0] is not None else 0
        }
        
        if con_graficas and master:
            generar_graficas(resultado, master)
            
        return resultado
    except Exception as e:
        raise Exception(f"Error al obtener estadísticas: {str(e)}")

def generar_graficas(datos, master):
    # Configuración de estilo
    plt.style.use('ggplot')
    
    # Figura para libros
    fig_libros = plt.Figure(figsize=(6, 4), dpi=100)
    ax_libros = fig_libros.add_subplot(111)
    
    if datos['libros_mas_prestados']:
        libros = [x[1][:15] + '...' if len(x[1]) > 15 else x[1] for x in datos['libros_mas_prestados']]
        prestamos = [x[2] for x in datos['libros_mas_prestados']]
        
        ax_libros.bar(libros, prestamos, color='skyblue')
        ax_libros.set_title('Top 5 Libros más prestados')
        ax_libros.set_ylabel('Cantidad de préstamos')
        ax_libros.tick_params(axis='x', rotation=45)
    
    canvas_libros = FigureCanvasTkAgg(fig_libros, master=master)
    canvas_libros.draw()
    canvas_libros.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Figura para usuarios
    fig_usuarios = plt.Figure(figsize=(6, 4), dpi=100)
    ax_usuarios = fig_usuarios.add_subplot(111)
    
    if datos['usuarios_activos']:
        usuarios = [x[1][:15] + '...' if len(x[1]) > 15 else x[1] for x in datos['usuarios_activos']]
        transacciones = [x[2] for x in datos['usuarios_activos']]
        
        ax_usuarios.barh(usuarios, transacciones, color='lightgreen')
        ax_usuarios.set_title('Top 5 Usuarios más activos')
        ax_usuarios.set_xlabel('Cantidad de transacciones')
    
    canvas_usuarios = FigureCanvasTkAgg(fig_usuarios, master=master)
    canvas_usuarios.draw()
    canvas_usuarios.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)