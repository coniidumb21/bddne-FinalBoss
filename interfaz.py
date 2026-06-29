# -*- coding: utf-8 -*-
import calendar
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
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
        resultado = callback_login(usuario, contrasenia)

        if resultado == "ok":
            root.destroy()
            abrir_seccion_admin(callback_login, db)
        elif resultado == "user_not_found":
            messagebox.showerror("Error", "Usuario no encontrado")
        elif resultado == "wrong_password":
            messagebox.showerror("Error", "Credenciales incorrectas")
        else:
            messagebox.showerror("Error", "Error al iniciar sesión")

    boton = tk.Button(root, text="Iniciar sesión", command=procesar_login, font=("Arial", 12, "bold"), bg="#FF66B3", fg="white", activebackground="#FF66B3", relief="flat", cursor="hand2")
    canvas.create_window(400, 470, width=180, height=38, window=boton)

    root.mainloop()


def abrir_seccion_admin(callback_login, db):
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

    # PANEL DE DATOS
    panel = tk.Frame(canvas_admin, bg="#F4C0E6", bd=0, highlightthickness=0)
    canvas_admin.create_window(400, 320, width=760, height=360, window=panel)

    # BOTONES CRUD SOBRE LA TABLA
    action_frame = tk.Frame(panel, bg="#F4C0E6", bd=0, highlightthickness=0)
    action_frame.place(x=0, y=0, width=760, height=70)

    btn_agregar = tk.Button(action_frame, text="Agregar", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2", bd=0, width=12)
    btn_actualizar = tk.Button(action_frame, text="Editar", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2", bd=0, width=12)
    btn_eliminar = tk.Button(action_frame, text="Eliminar", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2", bd=0, width=12)
    btn_refrescar = tk.Button(action_frame, text="Actualizar", font=("Arial", 10, "bold"), bg="#6c63ff", fg="white", activebackground="#554edb", relief="flat", cursor="hand2", bd=0, width=12)

    btn_agregar.pack(side="left", padx=14, pady=15)
    btn_actualizar.pack(side="left", padx=14, pady=15)
    btn_eliminar.pack(side="left", padx=14, pady=15)
    btn_refrescar.pack(side="left", padx=14, pady=15)

    # TABLA CON SCROLLBAR
    tabla_frame = tk.Frame(panel, bg="#F4C0E6", bd=0, highlightthickness=0)
    tabla_frame.place(x=0, y=72, width=720, height=288)

    tabla = ttk.Treeview(tabla_frame, show="headings", height=13)
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    tabla.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    current_tipo = {"value": "Clientes"}

    def mostrar_tabla(tipo):
        current_tipo["value"] = tipo
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

    def mostrar_mensaje(exito, texto, parent=None):
        if exito:
            messagebox.showinfo("Operación exitosa", texto, parent=parent)
        else:
            messagebox.showerror("Error", texto, parent=parent)

    def validar_email(valor):
        return "@" in valor and "." in valor and len(valor) >= 5

    def validar_fecha(valor):
        partes = valor.split("-")
        if len(partes) != 3:
            return False
        año, mes, dia = partes
        return año.isdigit() and mes.isdigit() and dia.isdigit() and 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31

    def validar_telefono(valor):
        return len(valor) >= 8 and all(c.isdigit() or c in "+ -()" for c in valor)

    def validar_campos(valores, reglas):
        for campo, reglas_campo in reglas.items():
            valor = valores.get(campo, "")
            if "required" in reglas_campo and not valor:
                raise ValueError(f"El campo '{campo}' es obligatorio.")
            if "numeric" in reglas_campo and valor and not valor.isdigit():
                raise ValueError(f"El campo '{campo}' debe contener solo números.")
            if "email" in reglas_campo and valor and not validar_email(valor):
                raise ValueError("Ingrese un email válido.")
            if "date" in reglas_campo and valor and not validar_fecha(valor):
                raise ValueError("Ingrese la fecha en formato AAAA-MM-DD.")
            if "phone" in reglas_campo and valor and not validar_telefono(valor):
                raise ValueError("Ingrese un teléfono válido.")

    def obtener_seleccion():
        seleccion = tabla.selection()
        if not seleccion:
            return None
        item = tabla.item(seleccion[0])
        columnas = tabla["columns"]
        return dict(zip(columnas, item["values"]))

    def abrir_formulario_campos(titulo, campos, callback, valores_iniciales=None):
        def abrir_calendario(entrada):
            def actualizar_calendario():
                for widget in frame_dias.winfo_children():
                    widget.destroy()
                mes_nombre.config(text=f"{calendar.month_name[mes_actual[0]]} {anio_actual[0]}")
                primer_dia, dias_mes = calendar.monthrange(anio_actual[0], mes_actual[0])
                dia_num = 1
                for fila in range(6):
                    for col in range(7):
                        if fila == 0 and col < primer_dia:
                            tk.Label(frame_dias, text="", width=4, bg="#F7F7F7").grid(row=fila, column=col)
                        elif dia_num > dias_mes:
                            tk.Label(frame_dias, text="", width=4, bg="#F7F7F7").grid(row=fila, column=col)
                        else:
                            boton_dia = tk.Button(frame_dias, text=str(dia_num), width=4, bg="#FFFFFF", relief="flat", command=lambda d=dia_num: seleccionar_fecha(d))
                            boton_dia.grid(row=fila, column=col, padx=1, pady=1)
                            dia_num += 1

            def seleccionar_fecha(dia):
                fecha = f"{anio_actual[0]:04d}-{mes_actual[0]:02d}-{dia:02d}"
                entrada.config(state="normal")
                entrada.delete(0, tk.END)
                entrada.insert(0, fecha)
                entrada.config(state="readonly")
                calendario.destroy()

            def mes_anterior():
                if mes_actual[0] == 1:
                    mes_actual[0] = 12
                    anio_actual[0] -= 1
                else:
                    mes_actual[0] -= 1
                actualizar_calendario()

            def mes_siguiente():
                if mes_actual[0] == 12:
                    mes_actual[0] = 1
                    anio_actual[0] += 1
                else:
                    mes_actual[0] += 1
                actualizar_calendario()

            try:
                fecha_obj = datetime.datetime.strptime(entrada.get().strip(), "%Y-%m-%d").date()
            except Exception:
                fecha_obj = datetime.date.today()
            anio_actual = [fecha_obj.year]
            mes_actual = [fecha_obj.month]

            calendario = tk.Toplevel(ventana)
            calendario.title("Seleccionar fecha")
            calendario.transient(ventana)
            calendario.grab_set()
            calendario.config(bg="#F7F7F7")
            calendario.resizable(False, False)

            header = tk.Frame(calendario, bg="#F7F7F7")
            header.pack(pady=8)
            tk.Button(header, text="<", command=mes_anterior, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)
            mes_nombre = tk.Label(header, text="", font=("Arial", 10, "bold"), bg="#F7F7F7")
            mes_nombre.pack(side="left", padx=8)
            tk.Button(header, text=">", command=mes_siguiente, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)

            dias_semana = tk.Frame(calendario, bg="#F7F7F7")
            dias_semana.pack()
            for idx, dia in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
                tk.Label(dias_semana, text=dia, width=4, font=("Arial", 9, "bold"), bg="#F7F7F7").grid(row=0, column=idx)

            frame_dias = tk.Frame(calendario, bg="#F7F7F7")
            frame_dias.pack(padx=8, pady=8)
            actualizar_calendario()

        ventana = tk.Toplevel(admin_root)
        ventana.title(titulo)
        ventana.geometry("480x360")
        ventana.resizable(False, False)
        ventana.config(bg="#F7F7F7")
        ventana.transient(admin_root)
        ventana.grab_set()
        ventana.focus_force()
        entradas = {}

        # Helper: placeholder text for Entry
        def set_placeholder(entry, text):
            default_fg = entry.cget("fg") if entry.cget("fg") else "black"
            had_readonly = (entry.cget('state') == 'readonly')
            if had_readonly:
                entry.config(state='normal')
            def on_focus_in(event):
                if entry.get() == text:
                    entry.delete(0, tk.END)
                    entry.config(fg=default_fg)
            def on_focus_out(event):
                if not entry.get():
                    if had_readonly:
                        entry.config(state='normal')
                    entry.insert(0, text)
                    entry.config(fg="#a9a9a9")
                    if had_readonly:
                        entry.config(state='readonly')
            entry.delete(0, tk.END)
            entry.insert(0, text)
            entry.config(fg="#a9a9a9")
            if had_readonly:
                entry.config(state='readonly')
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

        y_offset = 0
        for i, (etiqueta, ancho) in enumerate(campos):
            y = 24 + i * 40 + y_offset
            # keep plain label text; examples will be placeholders inside Entry
            tk.Label(ventana, text=etiqueta + ":", font=("Arial", 10, "bold"), bg="#F7F7F7").place(x=24, y=y)
            entry_width = ancho
            entrada = tk.Entry(ventana, font=("Arial", 10), width=entry_width, bd=1, relief="solid")
            # Make date fields readonly; they will be filled by the calendar
            if etiqueta in ("Fecha registro", "Fecha pedido"):
                entrada.config(state="readonly")
                entrada._was_readonly = True
            else:
                entrada._was_readonly = False
            entrada.place(x=180, y=y)
            if valores_iniciales and etiqueta in valores_iniciales:
                # populate initial values
                entrada.config(state="normal")
                entrada.delete(0, tk.END)
                entrada.insert(0, str(valores_iniciales[etiqueta]))
                if etiqueta in ("Fecha registro", "Fecha pedido"):
                    entrada.config(state="readonly")
            else:
                # set placeholders for certain fields
                if etiqueta == "RUT":
                    set_placeholder(entrada, "12345678-9")
                elif etiqueta == "Email":
                    set_placeholder(entrada, "ejemplo@correo.cl")
                elif etiqueta == "Teléfono":
                    set_placeholder(entrada, "+569 1234 5678")
                elif etiqueta in ("Fecha registro", "Fecha pedido"):
                    set_placeholder(entrada, "AAAA-MM-DD")
            entradas[etiqueta] = entrada
            if etiqueta in ("Fecha registro", "Fecha pedido"):
                # smaller calendar button so it doesn't overlap the entry
                tk.Button(ventana, text="Calend.", font=("Arial", 8, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2", command=lambda e=entrada: abrir_calendario(e)).place(x=390, y=y-2, width=70, height=24)
            if etiqueta in ("ID Cliente", "ID Pedido"):
                tk.Label(ventana, text="En caso de no ingresar un ID, se asignara uno automaticamente", font=("Arial", 8), bg="#F7F7F7", fg="#333333").place(x=180, y=y + 24)
                y_offset += 24

        def procesar():
            valores = {clave: entrada.get().strip() for clave, entrada in entradas.items()}
            try:
                exito = callback(valores)
            except Exception as e:
                mostrar_mensaje(False, str(e), parent=ventana)
                return
            if exito:
                ventana.destroy()
                mostrar_tabla(current_tipo["value"])

        tk.Button(ventana, text="Guardar", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", command=procesar).place(x=190, y=320, width=100, height=32)

    def agregar_cliente():
        reglas = {
            "RUT": ["required"],
            "Nombre": ["required"],
            "Email": ["required", "email"],
            "Fecha registro": ["required", "date"],
            "Dirección": ["required"],
            "Teléfono": ["required", "phone"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            cliente = {
                "cliente_id": db.obtener_siguiente_cliente_id(),
                "rut_cliente": valores["RUT"],
                "nombre": valores["Nombre"],
                "email": valores["Email"],
                "fecha_registro": valores["Fecha registro"],
                "direccion": valores["Dirección"],
                "telefono": valores["Teléfono"]
            }
            db.insertar_cliente(cliente)
            mostrar_mensaje(True, f"Cliente agregado correctamente. ID asignado: {cliente['cliente_id']}")
            return True

        abrir_formulario_campos("Agregar cliente", [("RUT", 28), ("Nombre", 28), ("Email", 28), ("Fecha registro", 28), ("Dirección", 28), ("Teléfono", 28)], callback)

    def editar_cliente():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un cliente en la tabla para editar.")
            return

        reglas = {
            "ID Cliente": ["required"],
            "RUT": ["required"],
            "Nombre": ["required"],
            "Email": ["required", "email"],
            "Fecha registro": ["required", "date"],
            "Dirección": ["required"],
            "Teléfono": ["required", "phone"]
        }

        valores_iniciales = {
            "ID Cliente": seleccion["cliente_id"],
            "RUT": seleccion["rut_cliente"],
            "Nombre": seleccion["nombre"],
            "Email": seleccion["email"],
            "Fecha registro": seleccion["fecha_registro"],
            "Dirección": seleccion["direccion"],
            "Teléfono": seleccion["telefono"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            cliente = {
                "cliente_id": valores["ID Cliente"],
                "rut_cliente": valores["RUT"],
                "nombre": valores["Nombre"],
                "email": valores["Email"],
                "fecha_registro": valores["Fecha registro"],
                "direccion": valores["Dirección"],
                "telefono": valores["Teléfono"]
            }
            db.editar_cliente(seleccion["rut_cliente"], cliente)
            mostrar_mensaje(True, "Cliente editado correctamente")
            return True

        abrir_formulario_campos("Editar cliente", [("ID Cliente", 28), ("RUT", 28), ("Nombre", 28), ("Email", 28), ("Fecha registro", 28), ("Dirección", 28), ("Teléfono", 28)], callback, valores_iniciales)

    def eliminar_cliente():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un cliente en la tabla para eliminar.")
            return

        pedidos_por_cliente = db.contar_pedidos_cliente(seleccion["cliente_id"])
        if pedidos_por_cliente > 0:
            texto = f"Este cliente tiene {pedidos_por_cliente} pedido(s). Al eliminarlo también se eliminarán sus pedidos asociados. ¿Desea continuar?"
        else:
            texto = "¿Está seguro de que desea eliminar este cliente?"

        if not messagebox.askyesno("Confirmar eliminación", texto):
            return

        try:
            if pedidos_por_cliente > 0:
                eliminados = db.eliminar_cliente_con_pedidos(seleccion["rut_cliente"], seleccion["cliente_id"])
                mostrar_mensaje(True, f"Cliente eliminado correctamente. Se eliminaron {eliminados} pedido(s) asociados.")
            else:
                db.eliminar_cliente(seleccion["rut_cliente"])
                mostrar_mensaje(True, "Cliente eliminado correctamente")
            mostrar_tabla(current_tipo["value"])
        except Exception as e:
            mostrar_mensaje(False, str(e))

    def agregar_producto():
        reglas = {
            "ID Producto": ["required", "numeric"],
            "Nombre": ["required"],
            "Descripción": ["required"],
            "Precio": ["required", "numeric"],
            "Stock": ["required", "numeric"],
            "Categoría": ["required"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            producto = {
                "producto_id": int(valores["ID Producto"]),
                "nombre": valores["Nombre"],
                "descripcion": valores["Descripción"],
                "precio": int(valores["Precio"]),
                "stock": int(valores["Stock"]),
                "categoria": valores["Categoría"]
            }
            db.insertar_producto(producto)
            mostrar_mensaje(True, "Producto agregado correctamente")
            return True

        abrir_formulario_campos("Agregar producto", [("ID Producto", 18), ("Nombre", 28), ("Descripción", 28), ("Precio", 18), ("Stock", 18), ("Categoría", 18)], callback)

    def editar_producto():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un producto en la tabla para editar.")
            return

        reglas = {
            "ID Producto": ["required", "numeric"],
            "Nombre": ["required"],
            "Descripción": ["required"],
            "Precio": ["required", "numeric"],
            "Stock": ["required", "numeric"],
            "Categoría": ["required"]
        }

        valores_iniciales = {
            "ID Producto": seleccion["producto_id"],
            "Nombre": seleccion["nombre"],
            "Descripción": seleccion["descripcion"],
            "Precio": seleccion["precio"].replace("$", "") if isinstance(seleccion["precio"], str) else seleccion["precio"],
            "Stock": seleccion["stock"],
            "Categoría": seleccion["categoria"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            producto = {
                "producto_id": int(valores["ID Producto"]),
                "nombre": valores["Nombre"],
                "descripcion": valores["Descripción"],
                "precio": int(valores["Precio"]),
                "stock": int(valores["Stock"]),
                "categoria": valores["Categoría"]
            }
            db.editar_producto(int(seleccion["producto_id"]), producto)
            mostrar_mensaje(True, "Producto editado correctamente")
            return True

        abrir_formulario_campos("Editar producto", [("ID Producto", 18), ("Nombre", 28), ("Descripción", 28), ("Precio", 18), ("Stock", 18), ("Categoría", 18)], callback, valores_iniciales)

    def eliminar_producto():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un producto en la tabla para eliminar.")
            return

        if not messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este producto?"):
            return

        try:
            db.eliminar_producto(int(seleccion["producto_id"]))
            mostrar_mensaje(True, "Producto eliminado correctamente")
            mostrar_tabla(current_tipo["value"])
        except Exception as e:
            mostrar_mensaje(False, str(e))

    def agregar_pedido():
        reglas = {
            "ID Pedido": ["required"],
            "ID Cliente": ["required"],
            "Fecha pedido": ["required", "date"],
            "Monto total": ["required", "numeric"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            pedido = {
                "pedido_id": valores["ID Pedido"],
                "cliente_id": valores["ID Cliente"],
                "fecha_pedido": valores["Fecha pedido"],
                "monto_total": int(valores["Monto total"]),
                "productos": []
            }
            db.insertar_pedido(pedido)
            mostrar_mensaje(True, "Pedido agregado correctamente")
            return True

        abrir_formulario_campos("Agregar pedido", [("ID Pedido", 18), ("ID Cliente", 18), ("Fecha pedido", 18), ("Monto total", 18)], callback)

    def editar_pedido():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un pedido en la tabla para editar.")
            return

        reglas = {
            "ID Pedido": ["required"],
            "ID Cliente": ["required"],
            "Fecha pedido": ["required", "date"],
            "Monto total": ["required", "numeric"]
        }

        valores_iniciales = {
            "ID Pedido": seleccion["pedido_id"],
            "ID Cliente": seleccion["cliente_id"],
            "Fecha pedido": seleccion["fecha_pedido"],
            "Monto total": seleccion["monto_total"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            pedido = {
                "cliente_id": valores["ID Cliente"],
                "fecha_pedido": valores["Fecha pedido"],
                "monto_total": int(valores["Monto total"])
            }
            db.editar_pedido(seleccion["pedido_id"], pedido)
            mostrar_mensaje(True, "Pedido editado correctamente")
            return True

        abrir_formulario_campos("Editar pedido", [("ID Pedido", 18), ("ID Cliente", 18), ("Fecha pedido", 18), ("Monto total", 18)], callback, valores_iniciales)

    def eliminar_pedido():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un pedido en la tabla para eliminar.")
            return

        if not messagebox.askyesno("Confirmar eliminación", "¿Está seguro de que desea eliminar este pedido?"):
            return

        try:
            db.eliminar_pedido(seleccion["pedido_id"])
            mostrar_mensaje(True, "Pedido eliminado correctamente")
            mostrar_tabla(current_tipo["value"])
        except Exception as e:
            mostrar_mensaje(False, str(e))

    def actualizar_botones_seccion():
        tipo = current_tipo["value"]
        if tipo == "Clientes":
            btn_agregar.config(command=agregar_cliente)
            btn_actualizar.config(command=editar_cliente)
            btn_eliminar.config(command=eliminar_cliente)
        elif tipo == "Productos":
            btn_agregar.config(command=agregar_producto)
            btn_actualizar.config(command=editar_producto)
            btn_eliminar.config(command=eliminar_producto)
        elif tipo == "Pedidos":
            btn_agregar.config(command=agregar_pedido)
            btn_actualizar.config(command=editar_pedido)
            btn_eliminar.config(command=eliminar_pedido)
        btn_refrescar.config(command=lambda: mostrar_tabla(current_tipo["value"]))

    def seleccionar_tipo(tipo):
        mostrar_tabla(tipo)
        actualizar_botones_seccion()

    # ----------------------------------------------------
    btn_clientes = tk.Button(admin_root, text="Clientes", command=lambda: seleccionar_tipo("Clientes"), font=("Arial", 10, "bold"), bg="#d80f69", fg="white", activebackground="#FF66B3", activeforeground="white", relief="flat", cursor="hand2")
    canvas_admin.create_window(451, 86, width=94, height=28, window=btn_clientes)

    btn_productos = tk.Button(admin_root, text="Productos", command=lambda: seleccionar_tipo("Productos"), font=("Arial", 10, "bold"), bg="#d80f69", fg="white", activebackground="#FF66B3", activeforeground="white", relief="flat", cursor="hand2")
    canvas_admin.create_window(578, 86, width=94, height=28, window=btn_productos)

    btn_pedidos = tk.Button(admin_root, text="Pedidos", command=lambda: seleccionar_tipo("Pedidos"), font=("Arial", 10, "bold"), bg="#d80f69", fg="white", activebackground="#FF66B3", activeforeground="white", relief="flat", cursor="hand2")
    canvas_admin.create_window(705, 86, width=93, height=28, window=btn_pedidos)

    def cerrar_sesion():
        admin_root.destroy()
        ejecutar_interfaz(callback_login, db)

    btn_cerrar_sesion = tk.Button(admin_root, text="Cerrar Sesión", command=cerrar_sesion, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2")
    canvas_admin.create_window(560, 530, width=170, height=36, window=btn_cerrar_sesion)

    seleccionar_tipo("Clientes")

    admin_root.mainloop()