import calendar
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
    btn_ver_productos = tk.Button(action_frame, text="Ver productos", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2", bd=0, width=12)
    btn_refrescar = tk.Button(action_frame, text="Actualizar", font=("Arial", 10, "bold"), bg="#6c63ff", fg="white", activebackground="#554edb", relief="flat", cursor="hand2", bd=0, width=12)

    btn_agregar.pack(side="left", padx=14, pady=15)
    btn_actualizar.pack(side="left", padx=14, pady=15)
    btn_eliminar.pack(side="left", padx=14, pady=15)
    btn_ver_productos.pack(side="left", padx=14, pady=15)
    btn_refrescar.pack(side="left", padx=14, pady=15)
    
    # Ocultar botón Ver productos inicialmente (solo para Pedidos)
    btn_ver_productos.pack_forget()

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
            tabla["columns"] = ("pedido_id", "cliente_id", "fecha_pedido", "monto_total")
            for col in tabla["columns"]: 
                tabla.heading(col, text=col.upper())
                tabla.column(col, width=175, anchor="center")
                
            for pedido in db.mostrar_pedidos():
                tabla.insert("", "end", values=(
                    pedido.get("pedido_id", ""), 
                    pedido.get("cliente_id", ""), 
                    pedido.get("fecha_pedido", ""), 
                    f"${pedido.get('monto_total', 0)}"
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
                            tk.Label(frame_dias, text="", width=4, bg="#CAADEB").grid(row=fila, column=col)
                        elif dia_num > dias_mes:
                            tk.Label(frame_dias, text="", width=4, bg="#CAADEB").grid(row=fila, column=col)
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
            calendario.config(bg="#CAADEB")
            calendario.resizable(False, False)

            header = tk.Frame(calendario, bg="#CAADEB")
            header.pack(pady=8)
            tk.Button(header, text="<", command=mes_anterior, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)
            mes_nombre = tk.Label(header, text="", font=("Arial", 10, "bold"), bg="#CAADEB")
            mes_nombre.pack(side="left", padx=8)
            tk.Button(header, text=">", command=mes_siguiente, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)

            dias_semana = tk.Frame(calendario, bg="#CAADEB")
            dias_semana.pack()
            for idx, dia in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
                tk.Label(dias_semana, text=dia, width=4, font=("Arial", 9, "bold"), bg="#CAADEB").grid(row=0, column=idx)

            frame_dias = tk.Frame(calendario, bg="#CAADEB")
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
        for i, item in enumerate(campos):
            # Si el formulario viejo manda 2 datos, lo adaptamos automáticamente. Si manda 4, lo usa normal.
            if len(item) == 2:
                etiqueta, ancho = item
                tipo_campo = "entry"
                opciones = None
            else:
                etiqueta, ancho, tipo_campo, opciones = item

            y = 24 + i * 40 + y_offset
            tk.Label(ventana, text=etiqueta + ":", font=("Arial", 10, "bold"), bg="#F7F7F7").place(x=24, y=y)
            
            # Decidimos si pintar una caja de texto o un desplegable
            if tipo_campo == "combobox":
                entrada = ttk.Combobox(ventana, font=("Arial", 10), width=ancho - 3, values=opciones, state="readonly")
                if opciones:
                    entrada.current(0)  # Selecciona el primero por defecto
            else:
                entrada = tk.Entry(ventana, font=("Arial", 10), width=ancho, bd=1, relief="solid")
                if etiqueta in ("Fecha registro", "Fecha pedido"):
                    entrada.config(state="readonly")
                    entrada._was_readonly = True
                else:
                    entrada._was_readonly = False
                    
            entrada.place(x=180, y=y)
            
            if valores_iniciales and etiqueta in valores_iniciales:
                if tipo_campo == "combobox":
                    entrada.set(str(valores_iniciales[etiqueta]))
                else:
                    entrada.config(state="normal")
                    entrada.delete(0, tk.END)
                    entrada.insert(0, str(valores_iniciales[etiqueta]))
                    if etiqueta in ("Fecha registro", "Fecha pedido"):
                        entrada.config(state="readonly")
            else:
                if tipo_campo != "combobox":
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
            "RUT": ["required"],
            "Nombre": ["required"],
            "Email": ["required", "email"],
            "Fecha registro": ["required", "date"],
            "Dirección": ["required"],
            "Teléfono": ["required", "phone"]
        }

        valores_iniciales = {
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
                "cliente_id": seleccion["cliente_id"],
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

        abrir_formulario_campos("Editar cliente", [("RUT", 28), ("Nombre", 28), ("Email", 28), ("Fecha registro", 28), ("Dirección", 28), ("Teléfono", 28)], callback, valores_iniciales)

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
            "Nombre": ["required"],
            "Descripción": ["required"],
            "Precio": ["required", "numeric"],
            "Stock": ["required", "numeric"],
            "Categoría": ["required"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            producto = {
                "producto_id": db.obtener_siguiente_producto_id(),
                "nombre": valores["Nombre"],
                "descripcion": valores["Descripción"],
                "precio": int(valores["Precio"]),
                "stock": int(valores["Stock"]),
                "categoria": valores["Categoría"]
            }
            db.insertar_producto(producto)
            mostrar_mensaje(True, f"Producto agregado correctamente. ID asignado: {producto['producto_id']}")
            return True

        abrir_formulario_campos("Agregar producto", [("Nombre", 28), ("Descripción", 28), ("Precio", 18), ("Stock", 18), ("Categoría", 18)], callback)

    def editar_producto():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un producto en la tabla para editar.")
            return

        reglas = {
            "Nombre": ["required"],
            "Descripción": ["required"],
            "Precio": ["required", "numeric"],
            "Stock": ["required", "numeric"],
            "Categoría": ["required"]
        }

        valores_iniciales = {
            "Nombre": seleccion["nombre"],
            "Descripción": seleccion["descripcion"],
            "Precio": seleccion["precio"].replace("$", "") if isinstance(seleccion["precio"], str) else seleccion["precio"],
            "Stock": seleccion["stock"],
            "Categoría": seleccion["categoria"]
        }

        def callback(valores):
            validar_campos(valores, reglas)
            producto = {
                "producto_id": int(seleccion["producto_id"]),
                "nombre": valores["Nombre"],
                "descripcion": valores["Descripción"],
                "precio": int(valores["Precio"]),
                "stock": int(valores["Stock"]),
                "categoria": valores["Categoría"]
            }
            db.editar_producto(int(seleccion["producto_id"]), producto)
            mostrar_mensaje(True, "Producto editado correctamente")
            return True

        abrir_formulario_campos("Editar producto", [("Nombre", 28), ("Descripción", 28), ("Precio", 18), ("Stock", 18), ("Categoría", 18)], callback, valores_iniciales)

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
        # Ventana exclusiva para crear pedidos
        ventana = tk.Toplevel(admin_root)
        ventana.title("Crear Nuevo Pedido")
        ventana.geometry("600x580")
        ventana.config(bg="#CAADEB")
        ventana.transient(admin_root)
        ventana.grab_set()

        # --- DATOS BÁSICOS ---
        # ID Pedido con placeholder explicativo
        tk.Label(ventana, text="ID Pedido:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=20)
        entry_id = tk.Entry(ventana, width=20, font=("Arial", 10), bd=1, relief="solid", fg="#a9a9a9")
        entry_id.insert(0, "Se asignará automáticamente")
        entry_id.place(x=160, y=20)

        def on_id_focus_in(event):
            if entry_id.get() == "Se asignará automáticamente":
                entry_id.delete(0, tk.END)
                entry_id.config(fg="black")
        def on_id_focus_out(event):
            if not entry_id.get().strip():
                entry_id.insert(0, "Se asignará automáticamente")
                entry_id.config(fg="#a9a9a9")
        entry_id.bind("<FocusIn>", on_id_focus_in)
        entry_id.bind("<FocusOut>", on_id_focus_out)

        tk.Label(ventana, text="Cliente:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=60)
        clientes_bd = db.mostrar_clientes()
        opciones_clientes = [f"{c.get('cliente_id', '')} - {c.get('nombre', '')}" for c in clientes_bd]
        if not opciones_clientes: opciones_clientes = ["No hay clientes"]
        combo_cliente = ttk.Combobox(ventana, values=opciones_clientes, width=40, state="readonly")
        combo_cliente.place(x=160, y=60)
        if opciones_clientes: combo_cliente.current(0)

        # Fecha con calendario
        tk.Label(ventana, text="Fecha pedido:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=100)
        entry_fecha = tk.Entry(ventana, width=18, font=("Arial", 10), bd=1, relief="solid", state="readonly")
        entry_fecha.config(state="normal")
        entry_fecha.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        entry_fecha.config(state="readonly")
        entry_fecha.place(x=160, y=100)

        def abrir_calendario_pedido():
            def actualizar_cal():
                for widget in frame_dias.winfo_children():
                    widget.destroy()
                mes_nombre.config(text=f"{calendar.month_name[mes_actual[0]]} {anio_actual[0]}")
                primer_dia, dias_mes = calendar.monthrange(anio_actual[0], mes_actual[0])
                dia_num = 1
                for fila in range(6):
                    for col in range(7):
                        if fila == 0 and col < primer_dia:
                            tk.Label(frame_dias, text="", width=4, bg="#CAADEB").grid(row=fila, column=col)
                        elif dia_num > dias_mes:
                            tk.Label(frame_dias, text="", width=4, bg="#CAADEB").grid(row=fila, column=col)
                        else:
                            tk.Button(frame_dias, text=str(dia_num), width=4, bg="#CAADEB", relief="flat",
                                      command=lambda d=dia_num: seleccionar_dia(d)).grid(row=fila, column=col, padx=1, pady=1)
                            dia_num += 1

            def seleccionar_dia(dia):
                fecha = f"{anio_actual[0]:04d}-{mes_actual[0]:02d}-{dia:02d}"
                entry_fecha.config(state="normal")
                entry_fecha.delete(0, tk.END)
                entry_fecha.insert(0, fecha)
                entry_fecha.config(state="readonly")
                cal_win.destroy()

            def mes_anterior():
                if mes_actual[0] == 1: mes_actual[0] = 12; anio_actual[0] -= 1
                else: mes_actual[0] -= 1
                actualizar_cal()

            def mes_siguiente():
                if mes_actual[0] == 12: mes_actual[0] = 1; anio_actual[0] += 1
                else: mes_actual[0] += 1
                actualizar_cal()

            try:
                fecha_obj = datetime.datetime.strptime(entry_fecha.get().strip(), "%Y-%m-%d").date()
            except Exception:
                fecha_obj = datetime.date.today()
            anio_actual = [fecha_obj.year]
            mes_actual = [fecha_obj.month]

            cal_win = tk.Toplevel(ventana)
            cal_win.title("Seleccionar fecha")
            cal_win.transient(ventana)
            cal_win.grab_set()
            cal_win.config(bg="#CAADEB")
            cal_win.resizable(False, False)

            header = tk.Frame(cal_win, bg="#CAADEB")
            header.pack(pady=8)
            tk.Button(header, text="<", command=mes_anterior, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)
            mes_nombre = tk.Label(header, text="", font=("Arial", 10, "bold"), bg="#CAADEB")
            mes_nombre.pack(side="left", padx=8)
            tk.Button(header, text=">", command=mes_siguiente, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)

            dias_semana = tk.Frame(cal_win, bg="#CAADEB")
            dias_semana.pack()
            for idx, dia in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
                tk.Label(dias_semana, text=dia, width=4, font=("Arial", 9, "bold"), bg="#CAADEB").grid(row=0, column=idx)

            frame_dias = tk.Frame(cal_win, bg="#CAADEB")
            frame_dias.pack(padx=8, pady=8)
            actualizar_cal()

        tk.Button(ventana, text="📅 Calendario", font=("Arial", 8, "bold"), bg="#FF66B3", fg="white",
                  activebackground="#d80f69", relief="flat", cursor="hand2",
                  command=abrir_calendario_pedido).place(x=340, y=98, width=100, height=24)

        # --- CARRITO ---
        tk.Label(ventana, text="─── AÑADIR PRODUCTOS ───", bg="#CAADEB", font=("Arial", 10, "bold"), fg="#d80f69").place(x=160, y=140)
        tk.Label(ventana, text="Producto:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=175)
        productos_bd = db.mostrar_productos()
        opciones_productos = [f"{p.get('producto_id', '')} - {p.get('nombre', '')} - ${p.get('precio', 0)}" for p in productos_bd]
        combo_producto = ttk.Combobox(ventana, values=opciones_productos, width=38, state="readonly")
        combo_producto.place(x=90, y=175)

        tk.Label(ventana, text="Cant:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=430, y=175)
        entry_cant = tk.Entry(ventana, width=5, font=("Arial", 10), bd=1, relief="solid")
        entry_cant.insert(0, "1")
        entry_cant.place(x=470, y=175)

        carrito_compras = []
        tabla_carrito = ttk.Treeview(ventana, columns=("ID", "Nombre", "Cant", "Subtotal"), show="headings", height=6)
        for col in ("ID", "Nombre", "Cant", "Subtotal"):
            tabla_carrito.heading(col, text=col)
            tabla_carrito.column(col, width=120, anchor="center")
        tabla_carrito.place(x=20, y=255, width=560)
        lbl_total = tk.Label(ventana, text="Total Pedido: $0", bg="#CAADEB", font=("Arial", 12, "bold"), fg="#d80f69")
        lbl_total.place(x=350, y=430)

        def agregar_al_carrito():
            seleccion = combo_producto.get()
            if not seleccion: return
            partes = seleccion.split(" - ")
            p_id, p_nombre, p_precio = partes[0], partes[1], int(partes[2].replace("$", ""))
            cantidad = int(entry_cant.get())
            carrito_compras.append({"producto_id": p_id, "nombre": p_nombre, "cantidad": cantidad, "precio": p_precio})
            tabla_carrito.insert("", "end", values=(p_id, p_nombre, cantidad, f"${p_precio * cantidad}"))
            lbl_total.config(text=f"Total: ${sum(i['precio'] * i['cantidad'] for i in carrito_compras)}")

        tk.Button(ventana, text="+ Añadir al carrito", command=agregar_al_carrito,
                  font=("Arial", 9, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69",
                  relief="flat", cursor="hand2").place(x=180, y=210, width=150, height=28)

        def guardar_todo_el_pedido():
            if not carrito_compras: return
            
            # Recolectar valores y aplicar tus reglas
            id_valor = entry_id.get().strip()
            if id_valor == "Se asignará automáticamente":
                id_valor = ""
            valores = {
                "ID Pedido": id_valor,
                "Cliente": combo_cliente.get().strip(),
                "Fecha pedido": entry_fecha.get().strip(),
                "Monto total": str(sum(i['precio'] * i['cantidad'] for i in carrito_compras))
            }
            
            # Reglas que ya tenías definidas en otros formularios
            reglas = {
                "ID Pedido": [],
                "Cliente": ["required"],
                "Fecha pedido": ["required", "date"],
                "Monto total": ["required", "numeric"]
            }
            
            try:
                validar_campos(valores, reglas)
                pedido_final = {
                    "pedido_id": valores["ID Pedido"],
                    "cliente_id": valores["Cliente"].split(" - ")[0].strip(),
                    "fecha_pedido": valores["Fecha pedido"],
                    "monto_total": int(valores["Monto total"]),
                    "productos": carrito_compras
                }
                db.insertar_pedido(pedido_final)
                mostrar_mensaje(True, "Pedido creado exitosamente", parent=ventana)
                ventana.destroy()
                mostrar_tabla("Pedidos")
            except Exception as e:
                mostrar_mensaje(False, str(e), parent=ventana)

        tk.Button(ventana, text="Guardar Pedido", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", command=guardar_todo_el_pedido).place(x=200, y=510, width=200, height=35)

    def editar_pedido():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un pedido en la tabla para editar.")
            return

        # Obtener el pedido completo de la base de datos
        pedido_completo = None
        for pedido in db.mostrar_pedidos():
            if pedido.get("pedido_id") == seleccion["pedido_id"]:
                pedido_completo = pedido
                break

        # Ventana exclusiva para editar pedidos
        ventana = tk.Toplevel(admin_root)
        ventana.title("Editar Pedido")
        ventana.geometry("600x580")
        ventana.config(bg="#CAADEB")
        ventana.transient(admin_root)
        ventana.grab_set()

        # --- DATOS BÁSICOS ---
        tk.Label(ventana, text="ID Pedido:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=20)
        entry_id = tk.Entry(ventana, width=20, font=("Arial", 10), bd=1, relief="solid", state="readonly")
        entry_id.insert(0, seleccion["pedido_id"])
        entry_id.place(x=160, y=20)

        tk.Label(ventana, text="Cliente:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=60)
        clientes_bd = db.mostrar_clientes()
        opciones_clientes = [f"{c.get('cliente_id', '')} - {c.get('nombre', '')}" for c in clientes_bd]
        combo_cliente = ttk.Combobox(ventana, values=opciones_clientes, width=40, state="readonly")
        combo_cliente.place(x=160, y=60)
        
        # Establecer cliente actual seleccionado
        for idx, opcion in enumerate(opciones_clientes):
            if opcion.startswith(str(seleccion["cliente_id"])):
                combo_cliente.current(idx)
                break

        # Fecha con calendario
        tk.Label(ventana, text="Fecha pedido:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=100)
        entry_fecha = tk.Entry(ventana, width=18, font=("Arial", 10), bd=1, relief="solid", state="readonly")
        entry_fecha.config(state="normal")
        entry_fecha.insert(0, seleccion["fecha_pedido"])
        entry_fecha.config(state="readonly")
        entry_fecha.place(x=160, y=100)

        def abrir_calendario_editar():
            def actualizar_cal():
                for widget in frame_dias.winfo_children():
                    widget.destroy()
                mes_nombre.config(text=f"{calendar.month_name[mes_actual[0]]} {anio_actual[0]}")
                primer_dia, dias_mes = calendar.monthrange(anio_actual[0], mes_actual[0])
                dia_num = 1
                for fila in range(6):
                    for col in range(7):
                        if fila == 0 and col < primer_dia:
                            tk.Label(frame_dias, text="", width=4, bg="#CAADEB").grid(row=fila, column=col)
                        elif dia_num > dias_mes:
                            tk.Label(frame_dias, text="", width=4, bg="#CAADEB").grid(row=fila, column=col)
                        else:
                            tk.Button(frame_dias, text=str(dia_num), width=4, bg="#CAADEB", relief="flat",
                                      command=lambda d=dia_num: seleccionar_dia(d)).grid(row=fila, column=col, padx=1, pady=1)
                            dia_num += 1

            def seleccionar_dia(dia):
                fecha = f"{anio_actual[0]:04d}-{mes_actual[0]:02d}-{dia:02d}"
                entry_fecha.config(state="normal")
                entry_fecha.delete(0, tk.END)
                entry_fecha.insert(0, fecha)
                entry_fecha.config(state="readonly")
                cal_win.destroy()

            def mes_anterior():
                if mes_actual[0] == 1: mes_actual[0] = 12; anio_actual[0] -= 1
                else: mes_actual[0] -= 1
                actualizar_cal()

            def mes_siguiente():
                if mes_actual[0] == 12: mes_actual[0] = 1; anio_actual[0] += 1
                else: mes_actual[0] += 1
                actualizar_cal()

            try:
                fecha_obj = datetime.datetime.strptime(entry_fecha.get().strip(), "%Y-%m-%d").date()
            except Exception:
                fecha_obj = datetime.date.today()
            anio_actual = [fecha_obj.year]
            mes_actual = [fecha_obj.month]

            cal_win = tk.Toplevel(ventana)
            cal_win.title("Seleccionar fecha")
            cal_win.transient(ventana)
            cal_win.grab_set()
            cal_win.config(bg="#CAADEB")
            cal_win.resizable(False, False)

            header = tk.Frame(cal_win, bg="#CAADEB")
            header.pack(pady=8)
            tk.Button(header, text="<", command=mes_anterior, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)
            mes_nombre = tk.Label(header, text="", font=("Arial", 10, "bold"), bg="#CAADEB")
            mes_nombre.pack(side="left", padx=8)
            tk.Button(header, text=">", command=mes_siguiente, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", relief="flat", cursor="hand2").pack(side="left", padx=8)

            dias_semana = tk.Frame(cal_win, bg="#CAADEB")
            dias_semana.pack()
            for idx, dia in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
                tk.Label(dias_semana, text=dia, width=4, font=("Arial", 9, "bold"), bg="#CAADEB").grid(row=0, column=idx)

            frame_dias = tk.Frame(cal_win, bg="#CAADEB")
            frame_dias.pack(padx=8, pady=8)
            actualizar_cal()

        tk.Button(ventana, text="📅 Calendario", font=("Arial", 8, "bold"), bg="#FF66B3", fg="white",
                  activebackground="#d80f69", relief="flat", cursor="hand2",
                  command=abrir_calendario_editar).place(x=340, y=98, width=100, height=24)

        # --- CARRITO ---
        tk.Label(ventana, text="─── PRODUCTOS EN PEDIDO ───", bg="#CAADEB", font=("Arial", 10, "bold"), fg="#d80f69").place(x=160, y=140)
        tk.Label(ventana, text="Producto:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=20, y=175)
        productos_bd = db.mostrar_productos()
        opciones_productos = [f"{p.get('producto_id', '')} - {p.get('nombre', '')} - ${p.get('precio', 0)}" for p in productos_bd]
        combo_producto = ttk.Combobox(ventana, values=opciones_productos, width=38, state="readonly")
        combo_producto.place(x=90, y=175)

        tk.Label(ventana, text="Cant:", bg="#CAADEB", font=("Arial", 9, "bold")).place(x=430, y=175)
        entry_cant = tk.Entry(ventana, width=5, font=("Arial", 10), bd=1, relief="solid")
        entry_cant.insert(0, "1")
        entry_cant.place(x=470, y=175)

        carrito_compras = list(pedido_completo.get("productos", [])) if pedido_completo else []
        
        tabla_carrito = ttk.Treeview(ventana, columns=("ID", "Nombre", "Cant", "Subtotal"), show="headings", height=6)
        for col in ("ID", "Nombre", "Cant", "Subtotal"):
            tabla_carrito.heading(col, text=col)
            tabla_carrito.column(col, width=120, anchor="center")
        tabla_carrito.place(x=20, y=255, width=560)
        
        lbl_total = tk.Label(ventana, text="Total Pedido: $0", bg="#CAADEB", font=("Arial", 12, "bold"), fg="#d80f69")
        lbl_total.place(x=350, y=430)

        def actualizar_tabla_carrito():
            for item in tabla_carrito.get_children():
                tabla_carrito.delete(item)
            total = 0
            for i in carrito_compras:
                subtotal = int(i['cantidad']) * int(i['precio'])
                tabla_carrito.insert("", "end", values=(i['producto_id'], i['nombre'], i['cantidad'], f"${subtotal}"))
                total += subtotal
            lbl_total.config(text=f"Total Pedido: ${total}")

        def agregar_al_carrito_editar():
            seleccion_prod = combo_producto.get()
            if not seleccion_prod: return
            partes = seleccion_prod.split(" - ")
            p_id, p_nombre, p_precio = str(partes[0]).strip(), partes[1], int(partes[2].replace("$", ""))
            cantidad = int(entry_cant.get())
            
            # Buscar si ya existe el producto
            existe = False
            for prod in carrito_compras:
                if str(prod["producto_id"]) == str(p_id):
                    prod["cantidad"] += cantidad
                    existe = True
                    break
            
            if not existe:
                carrito_compras.append({"producto_id": p_id, "nombre": p_nombre, "cantidad": cantidad, "precio": p_precio})
            
            actualizar_tabla_carrito()
            entry_cant.delete(0, tk.END)
            entry_cant.insert(0, "1")

        def eliminar_del_carrito():
            seleccion_tabla = tabla_carrito.selection()
            if not seleccion_tabla:
                mostrar_mensaje(False, "Selecciona un producto para eliminar", parent=ventana)
                return
            
            item = tabla_carrito.item(seleccion_tabla[0])
            valores = item["values"]
            producto_id = str(valores[0]).strip()
            
            carrito_compras[:] = [p for p in carrito_compras if str(p["producto_id"]).strip() != producto_id]
            actualizar_tabla_carrito()

        def modificar_cantidad():
            seleccion_tabla = tabla_carrito.selection()
            if not seleccion_tabla:
                mostrar_mensaje(False, "Selecciona un producto para modificar", parent=ventana)
                return
            
            nueva_cantidad_str = tk.simpledialog.askstring("Modificar cantidad", "Ingresa la nueva cantidad:", parent=ventana)
            if nueva_cantidad_str and nueva_cantidad_str.isdigit():
                nueva_cantidad = int(nueva_cantidad_str)
                item = tabla_carrito.item(seleccion_tabla[0])
                valores = item["values"]
                producto_id = str(valores[0]).strip()
                
                for prod in carrito_compras:
                    if str(prod["producto_id"]).strip() == producto_id:
                        prod["cantidad"] = nueva_cantidad
                        break
                
                actualizar_tabla_carrito()

        tk.Button(ventana, text="+ Agregar", command=agregar_al_carrito_editar,
                  font=("Arial", 9, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69",
                  relief="flat", cursor="hand2").place(x=20, y=210, width=120, height=28)
        
        tk.Button(ventana, text="- Eliminar", command=eliminar_del_carrito,
                  font=("Arial", 9, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69",
                  relief="flat", cursor="hand2").place(x=150, y=210, width=120, height=28)
        
        tk.Button(ventana, text="Modificar cant.", command=modificar_cantidad,
                  font=("Arial", 9, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69",
                  relief="flat", cursor="hand2").place(x=280, y=210, width=120, height=28)

        actualizar_tabla_carrito()

        def guardar_todo_el_pedido_editado():
            if not carrito_compras:
                mostrar_mensaje(False, "El pedido debe tener al menos un producto", parent=ventana)
                return
            
            try:
                nuevo_cliente = combo_cliente.get().split(" - ")[0].strip()
                nueva_fecha = entry_fecha.get().strip()
                monto_total = sum(int(i['precio']) * int(i['cantidad']) for i in carrito_compras)
                
                pedido_editado = {
                    "cliente_id": nuevo_cliente,
                    "fecha_pedido": nueva_fecha,
                    "monto_total": monto_total,
                    "productos": carrito_compras
                }
                db.editar_pedido(seleccion["pedido_id"], pedido_editado)
                mostrar_mensaje(True, "Pedido editado exitosamente", parent=ventana)
                ventana.destroy()
                mostrar_tabla("Pedidos")
            except Exception as e:
                mostrar_mensaje(False, str(e), parent=ventana)

        tk.Button(ventana, text="Guardar cambios", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", command=guardar_todo_el_pedido_editado).place(x=150, y=510, width=300, height=35)

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

    def ver_productos_pedido():
        seleccion = obtener_seleccion()
        if not seleccion:
            mostrar_mensaje(False, "Selecciona primero un pedido en la tabla para ver sus productos.")
            return

        # Obtener el pedido completo de la base de datos para ver sus productos
        pedido_completo = None
        for pedido in db.mostrar_pedidos():
            if pedido.get("pedido_id") == seleccion["pedido_id"]:
                pedido_completo = pedido
                break

        if not pedido_completo or not pedido_completo.get("productos"):
            mostrar_mensaje(False, "Este pedido no tiene productos asociados.")
            return

        # Crear ventana para mostrar productos
        ventana = tk.Toplevel(admin_root)
        ventana.title(f"Productos - Pedido {seleccion['pedido_id']}")
        ventana.geometry("600x400")
        ventana.resizable(False, False)
        ventana.config(bg="#F7F7F7")
        ventana.transient(admin_root)
        ventana.grab_set()
        ventana.focus_force()

        # Título
        tk.Label(ventana, text=f"Productos del Pedido: {seleccion['pedido_id']}", font=("Arial", 12, "bold"), bg="#F7F7F7").pack(pady=10)
        
        # Tabla de productos
        tabla_productos = ttk.Treeview(ventana, columns=("ID", "Nombre", "Cantidad", "Precio", "Subtotal"), show="headings", height=15)
        tabla_productos.heading("ID", text="ID PRODUCTO")
        tabla_productos.heading("Nombre", text="NOMBRE")
        tabla_productos.heading("Cantidad", text="CANTIDAD")
        tabla_productos.heading("Precio", text="PRECIO")
        tabla_productos.heading("Subtotal", text="SUBTOTAL")
        
        tabla_productos.column("ID", width=80, anchor="center")
        tabla_productos.column("Nombre", width=150, anchor="center")
        tabla_productos.column("Cantidad", width=80, anchor="center")
        tabla_productos.column("Precio", width=100, anchor="center")
        tabla_productos.column("Subtotal", width=100, anchor="center")

        # Estilos de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#d80f69", foreground="white", font=("Arial", 9, "bold"))

        # Insertar productos
        for producto in pedido_completo.get("productos", []):
            subtotal = int(producto.get("cantidad", 0)) * int(producto.get("precio", 0))
            tabla_productos.insert("", "end", values=(
                producto.get("producto_id", ""),
                producto.get("nombre", ""),
                producto.get("cantidad", ""),
                f"${producto.get('precio', 0)}",
                f"${subtotal}"
            ))

        tabla_productos.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón cerrar
        tk.Button(ventana, text="Cerrar", font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", command=ventana.destroy).pack(pady=10)

    def actualizar_botones_seccion():
        tipo = current_tipo["value"]
        if tipo == "Clientes":
            btn_agregar.config(command=agregar_cliente)
            btn_actualizar.config(command=editar_cliente)
            btn_eliminar.config(command=eliminar_cliente)
            btn_ver_productos.pack_forget()
        elif tipo == "Productos":
            btn_agregar.config(command=agregar_producto)
            btn_actualizar.config(command=editar_producto)
            btn_eliminar.config(command=eliminar_producto)
            btn_ver_productos.pack_forget()
        elif tipo == "Pedidos":
            btn_agregar.config(command=agregar_pedido)
            btn_actualizar.config(command=editar_pedido)
            btn_eliminar.config(command=eliminar_pedido)
            btn_ver_productos.pack(side="left", padx=14, pady=15)
            btn_ver_productos.config(command=ver_productos_pedido)
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

    def respaldar_datos():
        try:
            destino = db.respaldar_datos()
            messagebox.showinfo("Respaldo completado", f"Respaldo guardado en:\n{destino}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo respaldar los datos:\n{e}")

    def cerrar_sesion():
        admin_root.destroy()
        ejecutar_interfaz(callback_login, db)

    btn_respaldo = tk.Button(admin_root, text="Respaldar datos", command=respaldar_datos, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2")
    canvas_admin.create_window(380, 530, width=170, height=36, window=btn_respaldo)

    btn_cerrar_sesion = tk.Button(admin_root, text="Cerrar Sesión", command=cerrar_sesion, font=("Arial", 10, "bold"), bg="#FF66B3", fg="white", activebackground="#d80f69", relief="flat", cursor="hand2")
    canvas_admin.create_window(560, 530, width=170, height=36, window=btn_cerrar_sesion)

    seleccionar_tipo("Clientes")

    admin_root.mainloop()