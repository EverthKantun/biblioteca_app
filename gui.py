import tkinter as tk
from tkinter import messagebox, simpledialog
from usuarios import insertar_usuario, obtener_usuarios, actualizar_usuario, eliminar_usuario
from libros import insertar_libro, obtener_libros, actualizar_libro, eliminar_libro, verificar_disponibilidad
from transacciones import registrar_prestamo, registrar_devolucion, obtener_estatus_libros

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
        ventana.title("Reportes")
        ventana.geometry("600x400")

        # Lista de estatus de libros
        tk.Label(ventana, text="Estatus de Libros", font=("Arial", 12)).pack(pady=5)
        
        lista_frame = tk.Frame(ventana)
        lista_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        lista_estatus = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, width=80)
        for libro in obtener_estatus_libros():
            estado = "Disponible" if libro[1] else "Prestado"
            lista_estatus.insert(tk.END, f"Libro ID: {libro[0]} - Estado: {estado}")
        lista_estatus.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=lista_estatus.yview)

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