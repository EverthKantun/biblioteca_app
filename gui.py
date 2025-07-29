import tkinter as tk
from tkinter import messagebox, simpledialog
from usuarios import insertar_usuario, obtener_usuarios, actualizar_usuario, eliminar_usuario
from libros import insertar_libro, obtener_libros, actualizar_libro, eliminar_libro, verificar_disponibilidad
from transacciones import registrar_prestamo, registrar_devolucion, obtener_estatus_libros
from estadisticas import obtener_estadisticas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("600x400")

        tk.Label(root, text="Sistema de Gestión de Biblioteca", font=("Arial", 16)).pack(pady=10)

        tk.Button(root, text="Gestionar Usuarios", width=25, command=self.gestionar_usuarios).pack(pady=5)
        tk.Button(root, text="Gestionar Libros", width=25, command=self.gestionar_libros).pack(pady=5)
        tk.Button(root, text="Gestionar Transacciones", width=25, command=self.gestionar_transacciones).pack(pady=5)
        tk.Button(root, text="Reportes", width=25, command=self.mostrar_reportes).pack(pady=5)
        tk.Button(root, text="Salir", width=25, command=root.quit).pack(pady=20)

    def get_input(self, title, prompt):
        return simpledialog.askstring(title, prompt)

    def gestionar_usuarios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestión de Usuarios")
        ventana.geometry("500x400")

        # Campos de entrada
        tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        nombre_entry = tk.Entry(ventana)
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Dirección:").grid(row=1, column=0, padx=5, pady=5)
        direccion_entry = tk.Entry(ventana)
        direccion_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        telefono_entry = tk.Entry(ventana)
        telefono_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        tk.Button(ventana, text="Registrar Usuario", command=lambda: self.registrar_usuario(
            nombre_entry.get(), direccion_entry.get(), telefono_entry.get()
        )).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Actualizar Usuario", command=lambda: self.actualizar_usuario(
            nombre_entry.get(), direccion_entry.get(), telefono_entry.get()
        )).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Eliminar Usuario", command=self.eliminar_usuario).grid(row=5, column=0, columnspan=2, pady=10)

        # Lista de usuarios
        lista_frame = tk.Frame(ventana)
        lista_frame.grid(row=6, column=0, columnspan=2)
        
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        lista_usuarios = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, width=50)
        for usuario in obtener_usuarios():
            lista_usuarios.insert(tk.END, f"ID: {usuario[0]} - {usuario[1]} - Tel: {usuario[3]}")
        lista_usuarios.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=lista_usuarios.yview)

    def registrar_usuario(self, nombre, direccion, telefono):
        try:
            if not nombre or not direccion or not telefono:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return
            
            insertar_usuario(nombre, direccion, telefono)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_usuario(self, nombre, direccion, telefono):
        try:
            cliente_id = self.get_input("Actualizar Usuario", "Ingrese el ID del usuario a actualizar:")
            if not cliente_id:
                return
                
            if not nombre or not direccion or not telefono:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return
            
            actualizar_usuario(int(cliente_id), nombre, direccion, telefono)
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_usuario(self):
        try:
            cliente_id = self.get_input("Eliminar Usuario", "Ingrese el ID del usuario a eliminar:")
            if not cliente_id:
                return
                
            eliminar_usuario(int(cliente_id))
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gestionar_libros(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestión de Libros")
        ventana.geometry("500x400")

        # Campos de entrada
        tk.Label(ventana, text="Título:").grid(row=0, column=0, padx=5, pady=5)
        titulo_entry = tk.Entry(ventana)
        titulo_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Autor:").grid(row=1, column=0, padx=5, pady=5)
        autor_entry = tk.Entry(ventana)
        autor_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Año:").grid(row=2, column=0, padx=5, pady=5)
        anio_entry = tk.Entry(ventana)
        anio_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        tk.Button(ventana, text="Registrar Libro", command=lambda: self.registrar_libro(
            titulo_entry.get(), autor_entry.get(), anio_entry.get()
        )).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Actualizar Libro", command=lambda: self.actualizar_libro(
            titulo_entry.get(), autor_entry.get(), anio_entry.get()
        )).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Eliminar Libro", command=self.eliminar_libro).grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Verificar Disponibilidad", command=self.verificar_disponibilidad).grid(row=6, column=0, columnspan=2, pady=10)

        # Lista de libros
        lista_frame = tk.Frame(ventana)
        lista_frame.grid(row=7, column=0, columnspan=2)
        
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        lista_libros = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, width=50)
        for libro in obtener_libros():
            lista_libros.insert(tk.END, f"ID: {libro[0]} - {libro[1]} - {libro[2]} ({libro[3]})")
        lista_libros.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=lista_libros.yview)

    def registrar_libro(self, titulo, autor, anio):
        try:
            if not titulo or not autor or not anio:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return
                
            insertar_libro(titulo, autor, int(anio))
            messagebox.showinfo("Éxito", "Libro registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_libro(self, titulo, autor, anio):
        try:
            libro_id = self.get_input("Actualizar Libro", "Ingrese el ID del libro a actualizar:")
            if not libro_id:
                return
                
            if not titulo or not autor or not anio:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return
                
            actualizar_libro(int(libro_id), titulo, autor, int(anio))
            messagebox.showinfo("Éxito", "Libro actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_libro(self):
        try:
            libro_id = self.get_input("Eliminar Libro", "Ingrese el ID del libro a eliminar:")
            if not libro_id:
                return
                
            eliminar_libro(int(libro_id))
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def verificar_disponibilidad(self):
        try:
            libro_id = self.get_input("Verificar Disponibilidad", "Ingrese el ID del libro:")
            if not libro_id:
                return
                
            disponible = verificar_disponibilidad(int(libro_id))
            estado = "Disponible" if disponible else "No disponible (Prestado)"
            messagebox.showinfo("Disponibilidad", f"El libro ID {libro_id} está: {estado}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gestionar_transacciones(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestión de Transacciones")
        ventana.geometry("500x300")

        # Campos de entrada
        tk.Label(ventana, text="ID Usuario:").grid(row=0, column=0, padx=5, pady=5)
        usuario_entry = tk.Entry(ventana)
        usuario_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="ID Libro:").grid(row=1, column=0, padx=5, pady=5)
        libro_entry = tk.Entry(ventana)
        libro_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botones
        tk.Button(ventana, text="Registrar Préstamo", command=lambda: self.registrar_transaccion(
            usuario_entry.get(), libro_entry.get(), "PRÉSTAMO"
        )).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(ventana, text="Registrar Devolución", command=lambda: self.registrar_transaccion(
            usuario_entry.get(), libro_entry.get(), "DEVOLUCIÓN"
        )).grid(row=3, column=0, columnspan=2, pady=10)

    def registrar_transaccion(self, usuario_id, libro_id, tipo):
        try:
            if not usuario_id or not libro_id:
                messagebox.showwarning("Error", "Todos los campos son obligatorios")
                return
                
            if tipo == "PRÉSTAMO":
                registrar_prestamo(int(usuario_id), int(libro_id))
                messagebox.showinfo("Éxito", "Préstamo registrado correctamente")
            elif tipo == "DEVOLUCIÓN":
                registrar_devolucion(int(usuario_id), int(libro_id))
                messagebox.showinfo("Éxito", "Devolución registrada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_reportes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Reportes Complejos")
        ventana.geometry("1100x800")
        ventana.configure(bg='#f0f0f0')

        # Frame principal con pestañas manuales
        frame_pestanas = tk.Frame(ventana, bg='#f0f0f0')
        frame_pestanas.pack(pady=10)

        # Botones de pestañas
        btn_estado = tk.Button(frame_pestanas, text="Estado de Libros", width=20,
                            command=lambda: mostrar_pestana(0), relief='sunken')
        btn_estado.grid(row=0, column=0, padx=5)

        btn_estadisticas = tk.Button(frame_pestanas, text="Estadísticas", width=20,
                                command=lambda: mostrar_pestana(1))
        btn_estadisticas.grid(row=0, column=1, padx=5)

        # Contenedor de contenido
        frame_contenido = tk.Frame(ventana, bg='white', bd=2, relief='groove')
        frame_contenido.pack(fill='both', expand=True, padx=10, pady=(0,10))

        # Frame para estado de libros
        frame_estado = tk.Frame(frame_contenido, bg='white')
        frame_estado.pack(fill='both', expand=True)

        # Frame para estadísticas
        frame_stats = tk.Frame(frame_contenido, bg='white')
        
        # Lista para almacenar widgets de matplotlib
        figuras = []

        def mostrar_pestana(index):
            # Ocultar todas las pestañas
            frame_estado.pack_forget()
            frame_stats.pack_forget()
            
            # Resetear botones
            btn_estado.config(relief='raised')
            btn_estadisticas.config(relief='raised')
            
            # Mostrar pestaña seleccionada
            if index == 0:
                btn_estado.config(relief='sunken')
                frame_estado.pack(fill='both', expand=True)
                cargar_estado_libros()
            else:
                btn_estadisticas.config(relief='sunken')
                frame_stats.pack(fill='both', expand=True)
                cargar_estadisticas()

        def cargar_estado_libros():
            # Limpiar frame
            for widget in frame_estado.winfo_children():
                widget.destroy()
            
            # Frame con scroll
            canvas = tk.Canvas(frame_estado, bg='white')
            scrollbar = tk.Scrollbar(frame_estado, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='white')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Obtener y mostrar estado de libros
            try:
                libros = obtener_estatus_libros()
                if not libros:
                    tk.Label(scrollable_frame, text="No hay libros registrados", 
                            bg='white', font=('Arial', 12)).pack(pady=20)
                else:
                    tk.Label(scrollable_frame, text="ESTADO DE LIBROS", 
                            bg='white', font=('Arial', 14, 'bold')).pack(pady=10)
                    
                    # Encabezados
                    frame_header = tk.Frame(scrollable_frame, bg='#e0e0e0', bd=1, relief='groove')
                    frame_header.pack(fill='x', pady=(0,5), padx=10)
                    
                    tk.Label(frame_header, text="ID", width=8, anchor='w', 
                            bg='#e0e0e0', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
                    tk.Label(frame_header, text="ESTADO", width=15, anchor='w', 
                            bg='#e0e0e0', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
                    
                    # Datos
                    for libro in libros:
                        estado = "DISPONIBLE" if libro[1] else "PRESTADO"
                        color = '#d4edda' if libro[1] else '#f8d7da'
                        
                        frame_libro = tk.Frame(scrollable_frame, bg=color, bd=1, relief='groove')
                        frame_libro.pack(fill='x', pady=1, padx=10)
                        
                        tk.Label(frame_libro, text=f"{libro[0]}", width=8, anchor='w', 
                                bg=color, font=('Arial', 10)).pack(side='left', padx=5)
                        tk.Label(frame_libro, text=estado, width=15, anchor='w', 
                                bg=color, font=('Arial', 10)).pack(side='left', padx=5)
                        
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar los libros:\n{str(e)}")

        def cargar_estadisticas():
            # Limpiar frame y figuras anteriores
            for widget in frame_stats.winfo_children():
                widget.destroy()
            
            for fig in figuras:
                plt.close(fig)
            figuras.clear()
            
            try:
                from estadisticas import obtener_estadisticas
                stats = obtener_estadisticas()
                
                # Frame con scroll
                canvas = tk.Canvas(frame_stats, bg='white')
                scrollbar = tk.Scrollbar(frame_stats, orient='vertical', command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg='white')
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
                canvas.configure(yscrollcommand=scrollbar.set)
                
                canvas.pack(side='left', fill='both', expand=True)
                scrollbar.pack(side='right', fill='y')
                
                # Título
                tk.Label(scrollable_frame, text="ESTADÍSTICAS GENERALES", 
                        bg='white', font=('Arial', 14, 'bold')).pack(pady=10)
                
                # Gráfica de libros más prestados
                if stats['libros_mas_prestados']:
                    fig_libros = plt.Figure(figsize=(8, 4), dpi=100, facecolor='#f8f9fa')
                    ax_libros = fig_libros.add_subplot(111)
                    
                    libros = [x[1][:15] + '...' if len(x[1]) > 15 else x[1] for x in stats['libros_mas_prestados']]
                    prestamos = [x[2] for x in stats['libros_mas_prestados']]
                    
                    bars = ax_libros.bar(libros, prestamos, color='#007bff')
                    ax_libros.set_title('Libros más prestados', pad=20)
                    ax_libros.set_ylabel('Número de préstamos')
                    ax_libros.tick_params(axis='x', rotation=45)
                    
                    # Añadir valores en las barras
                    for bar in bars:
                        height = bar.get_height()
                        ax_libros.text(bar.get_x() + bar.get_width()/2., height,
                                    f'{int(height)}', ha='center', va='bottom')
                    
                    fig_libros.tight_layout()
                    
                    canvas_libros = FigureCanvasTkAgg(fig_libros, master=scrollable_frame)
                    canvas_libros.draw()
                    canvas_libros.get_tk_widget().pack(fill='x', padx=10, pady=5)
                    figuras.append(fig_libros)
                
                # Gráfica de usuarios más activos
                if stats['usuarios_activos']:
                    fig_usuarios = plt.Figure(figsize=(8, 4), dpi=100, facecolor='#f8f9fa')
                    ax_usuarios = fig_usuarios.add_subplot(111)
                    
                    usuarios = [x[1][:15] + '...' if len(x[1]) > 15 else x[1] for x in stats['usuarios_activos']]
                    transacciones = [x[2] for x in stats['usuarios_activos']]
                    
                    bars = ax_usuarios.barh(usuarios, transacciones, color='#28a745')
                    ax_usuarios.set_title('Usuarios más activos', pad=20)
                    ax_usuarios.set_xlabel('Número de transacciones')
                    
                    # Añadir valores en las barras
                    for bar in bars:
                        width = bar.get_width()
                        ax_usuarios.text(width, bar.get_y() + bar.get_height()/2.,
                                    f'{int(width)}', ha='left', va='center')
                    
                    fig_usuarios.tight_layout()
                    
                    canvas_usuarios = FigureCanvasTkAgg(fig_usuarios, master=scrollable_frame)
                    canvas_usuarios.draw()
                    canvas_usuarios.get_tk_widget().pack(fill='x', padx=10, pady=5)
                    figuras.append(fig_usuarios)
                
                # Mostrar porcentaje de disponibilidad
                frame_disponible = tk.Frame(scrollable_frame, bg='#fff3cd', bd=1, relief='groove')
                frame_disponible.pack(fill='x', padx=10, pady=10)
                
                tk.Label(frame_disponible, 
                        text=f"Tasa de disponibilidad general: {stats['porcentaje_disponible']}%",
                        bg='#fff3cd', font=('Arial', 12, 'bold')).pack(pady=10)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar las estadísticas:\n{str(e)}")
        
        # Mostrar primera pestaña por defecto
        mostrar_pestana(0)
        

def ejecutar_app():
    root = tk.Tk()
    app = BibliotecaApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nAplicación cerrada correctamente")
    finally:
        # Limpieza segura
        if 'app' in locals():
            for attr in ['ventana_usuarios', 'ventana_libros', 'ventana_transacciones']:
                if hasattr(app, attr):
                    getattr(app, attr).destroy()
            root.destroy()

if __name__ == "__main__":
    ejecutar_app()