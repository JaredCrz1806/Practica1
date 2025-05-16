import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Clases base
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Empleado(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)

class Sala:
    def __init__(self, nombre, tipo, capacidad):
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        self.disponibilidad = capacidad

class Pelicula:
    def __init__(self, titulo, duracion, clasificacion, genero):
        self.titulo = titulo
        self.duracion = duracion
        self.clasificacion = clasificacion
        self.genero = genero

class Funcion:
    def __init__(self, pelicula, sala, hora):
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora

class Reserva:
    def __init__(self, cliente, funcion, asientos):
        self.cliente = cliente
        self.funcion = funcion
        self.asientos = asientos

        if funcion.sala.disponibilidad >= asientos:
            funcion.sala.disponibilidad -= asientos
            self.exito = True
        else:
            self.exito = False

# Datos iniciales
salas = [Sala("Sala A", "IMAX", 100), Sala("Sala B", "3D", 80)]
peliculas = [
    Pelicula("Matrix", 136, "B15", "Acción"),
    Pelicula("Inception", 148, "B15", "Ciencia Ficción")
]
funciones = [
    Funcion(peliculas[0], salas[0], "18:00"),
    Funcion(peliculas[1], salas[1], "20:00")
]
reservas = []
empleado_actual = Empleado("")

# Funciones GUI
def cambiar_empleado():
    nombre = simpledialog.askstring("Cambiar Empleado", "Nombre del empleado:")
    if nombre:
        empleado_actual.nombre = nombre
        label_empleado.config(text=f"Empleado: {empleado_actual.nombre}")

def actualizar_funcion(event=None):
    titulo = combo_peliculas.get()
    funcion = next((f for f in funciones if f.pelicula.titulo == titulo), None)
    if funcion:
        label_sala.config(text=f"Sala: {funcion.sala.nombre} - Tipo: {funcion.sala.tipo}")
        label_hora.config(text=f"Horario: {funcion.hora}")
        label_disponibles.config(text=f"Asientos disponibles: {funcion.sala.disponibilidad}")

def agregar_funcion():
    titulo = simpledialog.askstring("Nueva Película", "Título:")
    if not titulo:
        return
    duracion = simpledialog.askinteger("Duración", "Duración en minutos:")
    clasificacion = simpledialog.askstring("Clasificación", "Clasificación:")
    genero = simpledialog.askstring("Género", "Género:")
    sala_nombre = simpledialog.askstring("Sala", "Nombre de la sala:")
    tipo_sala = simpledialog.askstring("Tipo de sala", "Ej: 2D, 3D, IMAX:")
    capacidad = simpledialog.askinteger("Capacidad", "Capacidad total:")
    hora = simpledialog.askstring("Hora", "Ej: 21:00")

    if not (titulo and duracion and clasificacion and genero and sala_nombre and tipo_sala and capacidad and hora):
        messagebox.showerror("Error", "Debes llenar todos los campos.")
        return

    sala = Sala(sala_nombre, tipo_sala, capacidad)
    salas.append(sala)
    nueva_peli = Pelicula(titulo, duracion, clasificacion, genero)
    peliculas.append(nueva_peli)
    nueva_funcion = Funcion(nueva_peli, sala, hora)
    funciones.append(nueva_funcion)

    combo_peliculas['values'] = [p.titulo for p in peliculas]
    combo_peliculas.set(titulo)
    actualizar_funcion()
    messagebox.showinfo("Función agregada", f"{titulo} agregada correctamente.")

def hacer_reserva():
    cliente = simpledialog.askstring("Nombre del cliente", "Cliente:")
    try:
        asientos = int(entry_asientos.get())
        titulo = combo_peliculas.get()
        funcion = next((f for f in funciones if f.pelicula.titulo == titulo), None)
        if funcion:
            reserva = Reserva(cliente, funcion, asientos)
            if reserva.exito:
                reservas.append(reserva)
                messagebox.showinfo("Reserva Exitosa", f"Reserva hecha para {cliente}.")
                actualizar_funcion()
            else:
                messagebox.showerror("Error", "No hay suficientes asientos.")
        else:
            messagebox.showerror("Error", "Función no encontrada.")
    except ValueError:
        messagebox.showerror("Error", "Asientos inválidos.")

def ver_historial():
    if reservas:
        texto = "\n".join([f"{r.cliente}: {r.asientos} asientos para {r.funcion.pelicula.titulo} a las {r.funcion.hora}" for r in reservas])
    else:
        texto = "No hay reservas registradas."
    messagebox.showinfo("Historial de Reservas", texto)

# GUI
ventana = tk.Tk()
ventana.title("Sistema de Reservas (Empleado)")
ventana.geometry("500x400")

label_empleado = tk.Label(ventana, text="Empleado: ", font=("Arial", 12))
label_empleado.pack(pady=10)
tk.Button(ventana, text="Cambiar empleado", command=cambiar_empleado).pack()

tk.Label(ventana, text="Selecciona película:").pack()
combo_peliculas = ttk.Combobox(ventana, values=[p.titulo for p in peliculas])
combo_peliculas.pack()
combo_peliculas.bind("<<ComboboxSelected>>", actualizar_funcion)
combo_peliculas.current(0)

label_sala = tk.Label(ventana, text="")
label_sala.pack()
label_hora = tk.Label(ventana, text="")
label_hora.pack()
label_disponibles = tk.Label(ventana, text="")
label_disponibles.pack(pady=5)

tk.Label(ventana, text="Asientos a reservar:").pack()
entry_asientos = tk.Entry(ventana)
entry_asientos.pack()

tk.Button(ventana, text="Hacer reserva", command=hacer_reserva).pack(pady=5)
tk.Button(ventana, text="Ver historial", command=ver_historial).pack(pady=5)
tk.Button(ventana, text="Agregar nueva función", command=agregar_funcion).pack(pady=5)

actualizar_funcion()
ventana.mainloop()
