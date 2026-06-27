import tkinter as tk
from PIL import Image, ImageTk

def ejecutar_interfaz():

    # ------------------------
    # Ventana
    # ------------------------
    root = tk.Tk()
    root.title("ComercioTech")
    root.geometry("800x600")
    root.resizable(False, False)

    # ------------------------
    # Imagen de fondo
    # ------------------------
    imagen = Image.open("assets/inicio-sesion.jpg")
    imagen = imagen.resize((800, 600))

    fondo = ImageTk.PhotoImage(imagen)

    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=fondo, anchor="nw")

    # ------------------------
    # Función del botón
    # ------------------------
    def iniciar_sesion():
        print("Usuario:", entry_usuario.get())
        print("Contraseña:", entry_password.get())

    # ------------------------
    # Entrada Usuario
    # ------------------------
    entry_usuario = tk.Entry(
        root,
        font=("Arial", 16),
        bg="#d80f69",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0
    )

    canvas.create_window(
        400,
        230,
        width=490,
        height=28,
        window=entry_usuario
    )

    # ------------------------
    # Entrada Contraseña
    # ------------------------
    entry_password = tk.Entry(
        root,
        font=("Arial", 16),
        bg="#d80f69",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0,
        show="*"
    )

    canvas.create_window(
        400,
        355,
        width=490,
        height=28,
        window=entry_password
    )

    # ------------------------
    # Botón
    # ------------------------
    boton = tk.Button(
        root,
        text="Iniciar sesión",
        command=iniciar_sesion,
        font=("Arial", 12, "bold"),
        bg="#FF66B3",
        fg="white",
        activebackground="#FF4DA6",
        relief="flat",
        cursor="hand2"
    )

    canvas.create_window(
        400,
        470,
        width=180,
        height=38,
        window=boton
    )

    root.mainloop()