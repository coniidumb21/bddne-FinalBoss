import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def ejecutar_interfaz(callback_login, db):
    # ----------------------------------------------------
    # VENTANA 1: INICIO DE SESIÓN
    # ----------------------------------------------------
    root = tk.Tk()
    root.title("ComercioTech - Iniciar Sesión")
    root.geometry("800x600")
    root.resizable(False, False)

    imagen = Image.open("assets/inicio-sesion.jpg")
    imagen = imagen.resize((800, 600))
    fondo = ImageTk.PhotoImage(imagen)

    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=fondo, anchor="nw")

    entry_usuario = tk.Entry(root, font=("Arial", 16), bg="#d80f69", fg="white", insertbackground="white", relief="flat", bd=0)
    canvas.create_window(400, 230, width=490, height=28, window=entry_usuario)

    entry_password = tk.Entry(root, font=("Arial", 16), bg="#d80f69", fg="white", insertbackground="white", relief="flat", bd=0, show="*")
    canvas.create_window(400, 355, width=490, height=28, window=entry_password)

    def procesar_login():
        usuario = entry_usuario.get().strip()
        contrasenia = entry_password.get().strip()
        
        if callback_login(usuario, contrasenia):
            root.destroy()
            abrir_seccion_admin(db)

    boton = tk.Button(root, text="Iniciar sesión", command=procesar_login, font=("Arial", 12, "bold"), bg="#FF66B3", fg="white", activebackground="#FF66B3", relief="flat", cursor="hand2")
    canvas.create_window(400, 470, width=180, height=38, window=boton)

    root.mainloop()


def abrir_seccion_admin(db):
    # ----------------------------------------------------
    # VENTANA 2: SECCIÓN ADMINISTRADOR
    # ----------------------------------------------------
    admin_root = tk.Tk()
    admin_root.title("ComercioTech - Panel de Administración")
    admin_root.geometry("800x600")
    admin_root.resizable(False, False)

    img_admin = Image.open("assets/seccion-admin.jpg")
    img_admin = img_admin.resize((800, 600))
    fondo_admin = ImageTk.PhotoImage(img_admin)

    canvas_admin = tk.Canvas(admin_root, width=800, height=600, highlightthickness=0)
    canvas_admin.pack(fill="both", expand=True)
    canvas_admin.create_image(0, 0, image=fondo_admin, anchor="nw")

    # ESTILOS DE LA TABLA
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", background="#d80f69", foreground="white", font=("Arial", 9, "bold"), relief="flat")
    style.map("Treeview.Heading", background=[("active", "#d80f69")])
    style.configure("Treeview", background="white", fieldbackground="white", foreground="black", rowheight=25, font=("Arial", 9))
    style.map("Treeview", background=[("selected", "#FF66B3")], foreground=[("selected", "white")])

    # CREAR TABLA
    tabla = ttk.Treeview(admin_root, show="headings")
    canvas_admin.create_window(400, 380, width=720, height=300, window=tabla)

    # ----------------------------------------------------
    # LÓGICA DINÁMICA DE LA TABLA (ESTRUCTURA EXACTA)
    # ----------------------------------------------------
    def mostrar_tabla(tipo):
        # Limpiar tabla actual
        for item in tabla.get_children():
            tabla.delete(item)
            
        if tipo == "Clientes":
            tabla["columns"] = ("cliente_id", "rut_cliente", "nombre", "email", "fecha_registro", "direccion", "telefono")
            for col in tabla["columns"]: 
                tabla.heading(col, text=col.upper())
                tabla.column(col, width=100, anchor="center")
            
            for cliente in db.mostrar_clientes():
                tabla.insert("", "end", values=(
                    cliente.get("cliente_id", ""), 
                    cliente.get("rut_cliente", ""), 
                    cliente.get("nombre", ""), 
                    cliente.get("email", ""), 
                    cliente.get("fecha_registro", ""), 
                    cliente.get("direccion", ""), 
                    cliente.get("telefono", "")
                ))

        elif tipo == "Productos":
            tabla["columns"] = ("producto_id", "nombre", "descripcion", "precio", "stock", "categoria")
            for col in tabla["columns"]: 
                tabla.heading(col, text=col.upper())
                tabla.column(col, width=120, anchor="center")
                
            for producto in db.mostrar_productos():
                tabla.insert("", "end", values=(
                    producto.get("producto_id", ""), 
                    producto.get("nombre", ""), 
                    producto.get("descripcion", ""), 
                    f"${producto.get('precio', 0)}", 
                    producto.get("stock", ""), 
                    producto.get("categoria", "")
                ))

        elif tipo == "Pedidos":
            tabla["columns"] = ("pedido_id", "cliente_id", "fecha_pedido", "monto_total", "productos")
            for col in tabla["columns"]: 
                tabla.heading(col, text=col.upper())
                tabla.column(col, width=140, anchor="center")
                
            for pedido in db.mostrar_pedidos():
                productos_pedido = str(pedido.get("productos", []))
                tabla.insert("", "end", values=(
                    pedido.get("pedido_id", ""), 
                    pedido.get("cliente_id", ""), 
                    pedido.get("fecha_pedido", ""), 
                    f"${pedido.get('monto_total', 0)}",
                    productos_pedido
                ))

    # ----------------------------------------------------
    btn_clientes = tk.Button(admin_root, text="Clientes", command=lambda: mostrar_tabla("Clientes"), font=("Arial", 10, "bold"), bg="#d80f69", fg="white", activebackground="#FF66B3", activeforeground="white", relief="flat", cursor="hand2")
    canvas_admin.create_window(451, 86, width=94, height=28, window=btn_clientes)

    btn_productos = tk.Button(admin_root, text="Productos", command=lambda: mostrar_tabla("Productos"), font=("Arial", 10, "bold"), bg="#d80f69", fg="white", activebackground="#FF66B3", activeforeground="white", relief="flat", cursor="hand2")
    canvas_admin.create_window(578, 86, width=94, height=28, window=btn_productos)

    btn_pedidos = tk.Button(admin_root, text="Pedidos", command=lambda: mostrar_tabla("Pedidos"), font=("Arial", 10, "bold"), bg="#d80f69", fg="white", activebackground="#FF66B3", activeforeground="white", relief="flat", cursor="hand2")
    canvas_admin.create_window(705, 86, width=93, height=28, window=btn_pedidos)

    admin_root.mainloop()