import tkinter as tk
from tkinter import messagebox
import re
import mysql.connector

def insertarRegistro(nombre, apellidos, edad, estatura, telefono, genero):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin_1234",
            database="mydb"
        )

        cursor = conexion.cursor()
        query = """
            INSERT INTO Registross
                (Nombre, Apellidos, Telefono, Estatura, Edad, Genero)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # El orden de las variables debe coincidir exactamente con las columnas de arriba
        valores = (nombre, apellidos, telefono, estatura, edad, genero)

        cursor.execute(query, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        messagebox.showinfo("Información", "Datos guardados en MySQL.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudieron guardar los datos:\n{err}")

def enteroValido(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

def decimalValido(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def telefonoValido(valor):
    return valor.isdigit() and len(valor) == 10

def textoValido(valor):
    return bool(re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", valor))

def borrar():
    tbNombre.delete(0, tk.END)
    tbApellidos.delete(0, tk.END)
    tbEdad.delete(0, tk.END)
    tbTelefono.delete(0, tk.END)
    tbEstatura.delete(0, tk.END)
    rbSeleccionGenero.set(0)

def guardar():
    nombre = tbNombre.get().strip()
    apellidos = tbApellidos.get().strip()
    edad = tbEdad.get().strip()
    telefono = tbTelefono.get().strip()
    estatura = tbEstatura.get().strip()

    genero = ""
    if rbSeleccionGenero.get() == 1:
        genero = "Masculino"
    elif rbSeleccionGenero.get() == 2:
        genero = "Femenino"
    elif rbSeleccionGenero.get() == 3:
        genero = "No definido"

    if not (
        enteroValido(edad)
        and decimalValido(estatura)
        and telefonoValido(telefono)
        and textoValido(nombre)
        and textoValido(apellidos)
        and genero
    ):
        messagebox.showerror(
            "Error",
            "Revisa los campos: nombre y apellidos deben ser texto, "
            "edad un número, estatura decimal, teléfono de 10 dígitos "
            "y debes seleccionar un género."
        )
        return

    insertarRegistro(
        nombre,
        apellidos,
        int(edad),
        float(estatura),
        telefono,
        genero
    )


ventana = tk.Tk()
ventana.configure(bg="#28A6C9")
ventana.geometry("350x550")
ventana.title("Actividad 04 - Formulario de Registro")

rbSeleccionGenero = tk.IntVar()

tk.Label(
    ventana, text="Nombre:", font=("Segoe UI", 14, "bold"), bg="#28A6C9"
).pack(padx=10, pady=8)
tbNombre = tk.Entry(ventana, width=35, justify="center")
tbNombre.pack()

tk.Label(
    ventana, text="Apellidos:", font=("Segoe UI", 14, "bold"), bg="#28A6C9"
).pack(padx=10, pady=8)
tbApellidos = tk.Entry(ventana, width=35, justify="center")
tbApellidos.pack()

tk.Label(
    ventana, text="Edad:", font=("Segoe UI", 14, "bold"), bg="#28A6C9"
).pack(padx=10, pady=8)
tbEdad = tk.Entry(ventana, width=10, justify="center")
tbEdad.pack()

tk.Label(
    ventana, text="Estatura:", font=("Segoe UI", 14, "bold"), bg="#28A6C9"
).pack(padx=10, pady=8)
tbEstatura = tk.Entry(ventana, width=15, justify="center")
tbEstatura.pack()

tk.Label(
    ventana, text="Teléfono:", font=("Segoe UI", 14, "bold"), bg="#28A6C9"
).pack(padx=10, pady=8)
tbTelefono = tk.Entry(ventana, width=35, justify="center")
tbTelefono.pack()

grupoGenero = tk.LabelFrame(
    ventana, text="Selecciona un género:", padx=10, pady=8, bg="#28A6C9"
)
grupoGenero.pack(padx=10, pady=8)

tk.Radiobutton(
    grupoGenero, text="Masculino", value=1, variable=rbSeleccionGenero, bg="#28A6C9"
).grid(column=1, row=1)

tk.Radiobutton(
    grupoGenero, text="Femenino", value=2, variable=rbSeleccionGenero, bg="#28A6C9"
).grid(column=2, row=1)

tk.Radiobutton(
    grupoGenero, text="No definido", value=3, variable=rbSeleccionGenero, bg="#28A6C9"
).grid(column=3, row=1)

grupoBotones = tk.LabelFrame(ventana, text="", bg="#28A6C9")
grupoBotones.pack(padx=10, pady=8)

tk.Button(
    grupoBotones, text="Guardar", width=10, padx=10, pady=8, command=guardar
).grid(column=1, row=1)

tk.Button(
    grupoBotones, text="Borrar", width=10, padx=10, pady=8, command=borrar
).grid(column=2, row=1)

ventana.mainloop()