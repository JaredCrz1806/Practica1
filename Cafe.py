
import tkinter as tk
from tkinter import messagebox, simpledialog

# Clases base
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Cliente(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.historial = []

class Empleado(Persona):
    def __init__(self, nombre, rol):
        super().__init__(nombre)
        self.rol = rol

class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamano, tipo, extras):
        super().__init__(nombre, precio)
        self.tamano = tamano
        self.tipo = tipo
        self.extras = extras

class Postre(ProductoBase):
    def __init__(self, nombre, precio, vegano, sin_gluten):
        super().__init__(nombre, precio)
        self.vegano = vegano
        self.sin_gluten = sin_gluten

class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []
        self.estado = "Pendiente"

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def total(self):
        return sum(p.precio for p in self.productos)

# Inventario simple
inventario = {
    "leche": 10,
    "azúcar": 20,
    "almendra": 5,
    "harina": 10
}

# Base de datos en memoria
clientes = []
pedidos = []

# GUI
ventana = tk.Tk()
ventana.title("Cafetería - Sistema de Pedidos")
ventana.geometry("500x500")

def nuevo_cliente():
    nombre = simpledialog.askstring("Cliente", "Nombre del cliente:")
    if nombre:
        cliente = Cliente(nombre)
        clientes.append(cliente)
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado.")

def hacer_pedido():
    nombre = simpledialog.askstring("Pedido", "Nombre del cliente:")
    cliente = next((c for c in clientes if c.nombre == nombre), None)
    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado.")
        return
    pedido = Pedido(cliente)

    tipo = simpledialog.askstring("Producto", "¿Bebida o Postre?")
    if tipo.lower() == "bebida":
        nombre_beb = simpledialog.askstring("Bebida", "Nombre:")
        tamano = simpledialog.askstring("Tamaño", "Pequeño, Mediano o Grande:")
        tipo_beb = simpledialog.askstring("Tipo", "Caliente o Fría:")
        extras = simpledialog.askstring("Extras", "Ej: sin azúcar, leche de almendra")
        producto = Bebida(nombre_beb, 40, tamano, tipo_beb, extras)

        if "leche" in extras and inventario["leche"] > 0:
            inventario["leche"] -= 1
        elif "leche" in extras:
            messagebox.showerror("Error", "No hay leche disponible.")
            return

    elif tipo.lower() == "postre":
        nombre_pos = simpledialog.askstring("Postre", "Nombre:")
        vegano = simpledialog.askstring("¿Vegano?", "Sí o No") == "Sí"
        sin_gluten = simpledialog.askstring("¿Sin gluten?", "Sí o No") == "Sí"
        producto = Postre(nombre_pos, 30, vegano, sin_gluten)

    else:
        messagebox.showerror("Error", "Producto inválido.")
        return

    pedido.agregar_producto(producto)
    pedidos.append(pedido)
    cliente.historial.append(pedido)
    messagebox.showinfo("Pedido", f"Pedido realizado. Total: ${pedido.total()}")

def ver_historial():
    nombre = simpledialog.askstring("Cliente", "Nombre del cliente:")
    cliente = next((c for c in clientes if c.nombre == nombre), None)
    if cliente and cliente.historial:
        texto = ""
        for p in cliente.historial:
            texto += f"- Pedido con {len(p.productos)} productos. Total: ${p.total()}\n"
        messagebox.showinfo("Historial", texto)
    else:
        messagebox.showinfo("Historial", "No hay pedidos.")

# Botones GUI
tk.Button(ventana, text="Registrar Cliente", command=nuevo_cliente).pack(pady=10)
tk.Button(ventana, text="Hacer Pedido", command=hacer_pedido).pack(pady=10)
tk.Button(ventana, text="Ver Historial Cliente", command=ver_historial).pack(pady=10)

ventana.mainloop()
