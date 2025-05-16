import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime, timedelta

class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Usuario(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.prestamos = []

class Bibliotecario(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)

class Material:
    def __init__(self, titulo, disponible=True):
        self.titulo = titulo
        self.disponible = disponible

class Libro(Material):
    def __init__(self, titulo, autor, genero):
        super().__init__(titulo)
        self.autor = autor
        self.genero = genero

class Prestamo:
    def __init__(self, usuario, material):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = self.fecha_prestamo + timedelta(days=7)
        self.devuelto = False
        self.penalizacion = 0

    def verificar_retraso(self):
        if not self.devuelto and datetime.now() > self.fecha_devolucion:
            self.penalizacion = (datetime.now() - self.fecha_devolucion).days * 5
        return self.penalizacion

usuarios = []
materiales = []
prestamos = []

# Ejemplo inicial
materiales.append(Libro("Cien años de soledad", "Gabriel García Márquez", "Novela"))

ventana = tk.Tk()
ventana.title("Gestión de Biblioteca (Bibliotecario)")
ventana.geometry("650x600")

def agregar_libro():
    titulo = simpledialog.askstring("Agregar Libro", "Título del libro:")
    autor = simpledialog.askstring("Agregar Libro", "Autor del libro:")
    genero = simpledialog.askstring("Agregar Libro", "Género del libro:")
    if titulo and autor and genero:
        materiales.append(Libro(titulo, autor, genero))
        messagebox.showinfo("Éxito", "Libro agregado correctamente.")

def eliminar_libro():
    titulos = [m.titulo for m in materiales if isinstance(m, Libro)]
    if not titulos:
        messagebox.showinfo("Info", "No hay libros para eliminar.")
        return
    libro = simpledialog.askstring("Eliminar Libro", "Título del libro a eliminar:")
    if libro:
        material = next((m for m in materiales if m.titulo == libro), None)
        if material:
            materiales.remove(material)
            messagebox.showinfo("Éxito", f"Libro '{libro}' eliminado.")
        else:
            messagebox.showerror("Error", "Libro no encontrado.")

def registrar_usuario():
    nombre = simpledialog.askstring("Registro", "Nombre del usuario:")
    if nombre:
        usuarios.append(Usuario(nombre))
        messagebox.showinfo("Éxito", f"Usuario {nombre} registrado.")

def prestar_libro():
    if not usuarios or not materiales:
        messagebox.showerror("Error", "Registra usuarios y libros primero.")
        return

    disponibles = [m for m in materiales if m.disponible]

    popup = tk.Toplevel()
    popup.title("Préstamo de Libro")
    popup.geometry("400x250")

    tk.Label(popup, text="Selecciona un usuario:").pack(pady=5)
    combo_usuario = ttk.Combobox(popup, values=[u.nombre for u in usuarios])
    combo_usuario.pack()
    combo_usuario.current(0)

    tk.Label(popup, text="Selecciona un libro disponible:").pack(pady=10)
    combo_libro = ttk.Combobox(popup, values=[m.titulo for m in disponibles])
    combo_libro.pack()
    combo_libro.current(0)

    def confirmar():
        nombre_usuario = combo_usuario.get()
        titulo_libro = combo_libro.get()
        usuario = next((u for u in usuarios if u.nombre == nombre_usuario), None)
        libro = next((m for m in materiales if m.titulo == titulo_libro and m.disponible), None)
        if usuario and libro:
            p = Prestamo(usuario, libro)
            usuario.prestamos.append(p)
            prestamos.append(p)
            libro.disponible = False
            messagebox.showinfo("Éxito", f"Libro prestado hasta {p.fecha_devolucion.date()}")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Préstamo fallido.")

    tk.Button(popup, text="Confirmar Préstamo", command=confirmar).pack(pady=15)

def devolver_libro():
    nombre = simpledialog.askstring("Devolver", "Nombre del usuario:")
    usuario = next((u for u in usuarios if u.nombre == nombre), None)
    if not usuario:
        messagebox.showerror("Error", "Usuario no encontrado.")
        return

    no_devueltos = [p for p in usuario.prestamos if not p.devuelto]
    if not no_devueltos:
        messagebox.showinfo("Info", "No hay préstamos pendientes.")
        return

    popup = tk.Toplevel()
    popup.title("Devolución de Libro")
    popup.geometry("400x250")

    tk.Label(popup, text="Selecciona el libro a devolver:").pack(pady=10)
    combo_libro = ttk.Combobox(popup, values=[p.material.titulo for p in no_devueltos])
    combo_libro.pack()
    combo_libro.current(0)

    def confirmar_devolucion():
        titulo = combo_libro.get()
        prestamo = next((p for p in no_devueltos if p.material.titulo == titulo), None)
        if prestamo:
            prestamo.devuelto = True
            prestamo.material.disponible = True
            penal = prestamo.verificar_retraso()
            if penal > 0:
                messagebox.showinfo("Multa", f"Devolución con multa: ${penal}")
            else:
                messagebox.showinfo("Éxito", "Libro devuelto sin penalización.")
            popup.destroy()

    tk.Button(popup, text="Confirmar Devolución", command=confirmar_devolucion).pack(pady=15)

def ver_prestamos():
    texto = ""
    for p in prestamos:
        estado = "Devuelto" if p.devuelto else "Pendiente"
        penal = p.verificar_retraso()
        texto += f"{p.usuario.nombre} - {p.material.titulo} - Dev: {p.fecha_devolucion.date()} - {estado}"
        if penal > 0:
            texto += f" - Multa: ${penal}"
        texto += "\n"
    if texto:
        messagebox.showinfo("Préstamos", texto)
    else:
        messagebox.showinfo("Préstamos", "No hay préstamos registrados.")

def ver_materiales():
    if materiales:
        lista = [f"{m.titulo} - {'Disponible' if m.disponible else 'Prestado'}" for m in materiales]
        messagebox.showinfo("Materiales", "\n".join(lista))
    else:
        messagebox.showinfo("Materiales", "No hay materiales en la biblioteca.")

# Interfaz de botones
tk.Label(ventana, text="Sistema de Biblioteca (Administrador)", font=("Helvetica", 16)).pack(pady=20)

tk.Button(ventana, text="Registrar Usuario", command=registrar_usuario).pack(pady=5)
tk.Button(ventana, text="Agregar Libro", command=agregar_libro).pack(pady=5)
tk.Button(ventana, text="Eliminar Libro", command=eliminar_libro).pack(pady=5)
tk.Button(ventana, text="Prestar Libro", command=prestar_libro).pack(pady=5)
tk.Button(ventana, text="Devolver Libro", command=devolver_libro).pack(pady=5)
tk.Button(ventana, text="Ver Préstamos", command=ver_prestamos).pack(pady=5)
tk.Button(ventana, text="Ver Materiales", command=ver_materiales).pack(pady=5)

ventana.mainloop()
