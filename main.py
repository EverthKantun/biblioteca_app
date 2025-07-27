import tkinter as tk
from tkinter import ttk, messagebox
from usuarios import insertar_usuario, actualizar_usuario, eliminar_usuario, obtener_usuarios
from libros import insertar_libro, actualizar_libro, eliminar_libro, obtener_libros, verificar_disponibilidad
from transacciones import registrar_prestamo, registrar_devolucion, obtener_estatus_libros

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")

        tab_control = ttk.Notebook(root)
        self.tab_usuarios = ttk.Frame(tab_control)
        self.tab_libros = ttk.Frame(tab_control)
        self.tab_transacciones = ttk.Frame(tab_control)
        self.tab_estatus = ttk.Frame(tab_control)

        tab_control.add(self.tab_usuarios, text='Usuarios')
        tab_control.add(self.tab_libros, text='Libros')
        tab_control.add(self.tab_transacciones, text='Transacciones')
        tab_control.add(self.tab_estatus, text='Estatus')
        tab_control.pack(expand=1, fill='both')

        self.setup_usuarios_tab()
        self.setup_libros_tab()
        self.setup_transacciones_tab()
        self.setup_estatus_tab()

    def setup_usuarios_tab(self):
        ttk.Label(self.tab_usuarios, text="Nombre:").grid(column=0, row=0)
        self.nombre_usuario = tk.Entry(self.tab_usuarios)
        self.nombre_usuario.grid(column=1, row=0)

        ttk.Button(self.tab_usuarios, text="Registrar Usuario", command=self.registrar_usuario).grid(column=0, row=1)
        ttk.Button(self.tab_usuarios, text="Actualizar Usuario", command=self.actualizar_usuario).grid(column=1, row=1)
        ttk.Button(self.tab_usuarios, text="Eliminar Usuario", command=self.eliminar_usuario).grid(column=2, row=1)

    def registrar_usuario(self):
        nombre = self.nombre_usuario.get()
        if nombre:
            insertar_usuario(nombre)
            messagebox.showinfo("Éxito", "Usuario registrado")

    def actualizar_usuario(self):
        user_id = simple_input("ID del usuario a actualizar:")
        nuevo_nombre = self.nombre_usuario.get()
        if user_id and nuevo_nombre:
            actualizar_usuario(user_id, nuevo_nombre)
            messagebox.showinfo("Éxito", "Usuario actualizado")

    def eliminar_usuario(self):
        user_id = simple_input("ID del usuario a eliminar:")
        if user_id:
            eliminar_usuario(user_id)
            messagebox.showinfo("Éxito", "Usuario eliminado")

    def setup_libros_tab(self):
        ttk.Label(self.tab_libros, text="Título:").grid(column=0, row=0)
        self.titulo_libro = tk.Entry(self.tab_libros)
        self.titulo_libro.grid(column=1, row=0)

        ttk.Label(self.tab_libros, text="Autor:").grid(column=0, row=1)
        self.autor_libro = tk.Entry(self.tab_libros)
        self.autor_libro.grid(column=1, row=1)

        ttk.Label(self.tab_libros, text="Categoría:").grid(column=0, row=2)
        self.categoria_libro = tk.Entry(self.tab_libros)
        self.categoria_libro.grid(column=1, row=2)

        ttk.Button(self.tab_libros, text="Registrar Libro", command=self.registrar_libro).grid(column=0, row=3)
        ttk.Button(self.tab_libros, text="Actualizar Libro", command=self.actualizar_libro).grid(column=1, row=3)
        ttk.Button(self.tab_libros, text="Eliminar Libro", command=self.eliminar_libro).grid(column=2, row=3)
        ttk.Button(self.tab_libros, text="Disponibilidad", command=self.verificar_disponibilidad).grid(column=0, row=4)

    def registrar_libro(self):
        insertar_libro(self.titulo_libro.get(), self.autor_libro.get(), self.categoria_libro.get())
        messagebox.showinfo("Éxito", "Libro registrado")

    def actualizar_libro(self):
        libro_id = simple_input("ID del libro a actualizar:")
        if libro_id:
            actualizar_libro(libro_id, self.titulo_libro.get(), self.autor_libro.get(), self.categoria_libro.get())
            messagebox.showinfo("Éxito", "Libro actualizado")

    def eliminar_libro(self):
        libro_id = simple_input("ID del libro a eliminar:")
        if libro_id:
            eliminar_libro(libro_id)
            messagebox.showinfo("Éxito", "Libro eliminado")

    def verificar_disponibilidad(self):
        libro_id = simple_input("ID del libro:")
        disponible = verificar_disponibilidad(libro_id)
        estado = "Disponible" if disponible else "Prestado"
        messagebox.showinfo("Disponibilidad", f"Libro está {estado}")

    def setup_transacciones_tab(self):
        ttk.Label(self.tab_transacciones, text="Cliente ID:").grid(column=0, row=0)
        self.cliente_id = tk.Entry(self.tab_transacciones)
        self.cliente_id.grid(column=1, row=0)

        ttk.Label(self.tab_transacciones, text="Libro ID:").grid(column=0, row=1)
        self.libro_id = tk.Entry(self.tab_transacciones)
        self.libro_id.grid(column=1, row=1)

        ttk.Button(self.tab_transacciones, text="Registrar Préstamo", command=self.registrar_prestamo).grid(column=0, row=2)
        ttk.Button(self.tab_transacciones, text="Registrar Devolución", command=self.registrar_devolucion).grid(column=1, row=2)

    def registrar_prestamo(self):
        registrar_prestamo(self.cliente_id.get(), self.libro_id.get())
        messagebox.showinfo("Éxito", "Préstamo registrado")

    def registrar_devolucion(self):
        registrar_devolucion(self.cliente_id.get(), self.libro_id.get())
        messagebox.showinfo("Éxito", "Devolución registrada")

    def setup_estatus_tab(self):
        ttk.Button(self.tab_estatus, text="Ver Estatus de Libros", command=self.ver_estatus).pack()

    def ver_estatus(self):
        estatus = obtener_estatus_libros()
        resultado = "\n".join([f"ID {e[0]}: {'Disponible' if e[1] else 'Prestado'}" for e in estatus])
        messagebox.showinfo("Estatus de Libros", resultado)


def simple_input(prompt):
    from tkinter.simpledialog import askstring
    return askstring("Entrada", prompt)

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
