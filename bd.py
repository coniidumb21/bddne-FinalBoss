from pymongo import MongoClient

class bd:
    def __init__(self):
        self.cliente = MongoClient("mongodb://localhost:27017")
        self.db = self.cliente["comercioTech"]
        self.admin = self.db["admin"]
        self.clientes = self.db["clientes"]
        self.productos = self.db["productos"]
        self.pedidos = self.db["pedidos"]

    # Verificar Admin
    def buscar_admin_por_usuario(self, usuario):
        return self.db["admin"].find_one({"usuario": usuario})

    def verificar_admin(self, usuario, contrasenia):
        admin = self.buscar_admin_por_usuario(usuario)
        return admin is not None and admin.get("contrasenia") == contrasenia
            
    # CRUD CLIENTES

    def obtener_siguiente_cliente_id(self):
        # Busca todos los clientes y extrae el número máximo del formato C00X
        ultimo_cliente = self.clientes.find_one(sort=[("cliente_id", -1)])
        max_num = 0
        
        if ultimo_cliente and "cliente_id" in ultimo_cliente:
            cliente_id = str(ultimo_cliente["cliente_id"])
            if cliente_id.startswith("C") and cliente_id[1:].isdigit():
                max_num = int(cliente_id[1:])
        
        nuevo_num = max_num + 1
        # Retorna el formato C seguido de 3 dígitos (ej: C001, C002, C010)
        return f"C{nuevo_num:03d}"

    def insertar_cliente(self, cliente):
        if "cliente_id" not in cliente or cliente["cliente_id"] in (None, ""):
            cliente["cliente_id"] = self.obtener_siguiente_cliente_id()
        else:
            try:
                cliente["cliente_id"] = int(cliente["cliente_id"])
            except (ValueError, TypeError):
                cliente["cliente_id"] = self.obtener_siguiente_cliente_id()

        self.clientes.insert_one(cliente)

    def mostrar_clientes(self):
        return list(self.clientes.find())
    
    def actualizar_cliente(self, rut, direccion):
        self.clientes.update_one(
            {"rut_cliente": rut},
            {"$set": {"direccion": direccion}}
        )

    def editar_cliente(self, rut, cliente):
        self.clientes.update_one(
            {"rut_cliente": rut},
            {"$set": cliente}
        )

    def eliminar_cliente(self, rut):
        self.clientes.delete_one(
            {"rut_cliente": rut}
        )

    def contar_pedidos_cliente(self, cliente_id):
        return self.pedidos.count_documents({"cliente_id": cliente_id})

    def eliminar_cliente_con_pedidos(self, rut_cliente, cliente_id):
        self.clientes.delete_one({"rut_cliente": rut_cliente})
        return self.pedidos.delete_many({"cliente_id": cliente_id}).deleted_count
        
    # CRUD PRODUCTOS

    def obtener_siguiente_producto_id(self):
        # Busca todos los productos y extrae el número máximo
        ultimo_producto = self.productos.find_one(sort=[("producto_id", -1)])
        max_num = 100  # Comenzamos en 100, el siguiente será 101
        
        if ultimo_producto and "producto_id" in ultimo_producto:
            try:
                product_id = int(ultimo_producto["producto_id"])
                if product_id > max_num:
                    max_num = product_id
            except (ValueError, TypeError):
                pass
        
        return max_num + 1

    def insertar_producto(self, producto):
        # Si no tiene producto_id o está vacío, generamos uno automáticamente
        if "producto_id" not in producto or producto["producto_id"] in (None, ""):
            producto["producto_id"] = self.obtener_siguiente_producto_id()
        else:
            try:
                producto["producto_id"] = int(producto["producto_id"])
            except (ValueError, TypeError):
                producto["producto_id"] = self.obtener_siguiente_producto_id()
        
        self.productos.insert_one(producto)

    def mostrar_productos(self):
        return list(self.productos.find())
    
    def actualizar_stock(self, producto_id, stock):
        self.productos.update_one(
            {"producto_id": producto_id},
            {"$set": {"stock": stock}}
        )
        
    def editar_producto(self, producto_id, producto):
        self.productos.update_one(
            {"producto_id": producto_id},
            {"$set": producto}
        )

    def eliminar_producto(self, producto_id):
        self.productos.delete_one(
            {"producto_id": producto_id}
        )
        
    # CRUD PEDIDOS
    # CRUD PEDIDOS

    def insertar_pedido(self, pedido):
        # Si el usuario dejó el ID en blanco, generamos uno automáticamente
        if "pedido_id" not in pedido or str(pedido["pedido_id"]).strip() == "":
            pedido["pedido_id"] = self.obtener_siguiente_pedido_id()
        
        # Insertamos directamente, sin forzar a que sea un número
        self.pedidos.insert_one(pedido)

    def obtener_siguiente_pedido_id(self):
        # Traemos todos los pedidos para calcular el siguiente número
        pedidos = list(self.pedidos.find({}, {"pedido_id": 1}))
        max_num = 0
        
        for p in pedidos:
            pid = str(p.get("pedido_id", ""))
            
            # Verificamos si empieza con 'P' y lo demás es número
            if pid.startswith("P") and pid[1:].isdigit():
                num = int(pid[1:])
                if num > max_num:
                    max_num = num
                    
            # Por si tienes números antiguos guardados (ej: 1, 2, 3)
            elif pid.isdigit():
                num = int(pid)
                if num > max_num:
                    max_num = num
                    
        nuevo_num = max_num + 1
        # Retorna el formato P seguido de 3 dígitos (ej: P001, P002, P010)
        return f"P{nuevo_num:03d}"

    def mostrar_pedidos(self):
        return list(self.pedidos.find())

    def actualizar_total(self, pedido_id, total):
        self.pedidos.update_one(
            {"pedido_id": pedido_id},
            {"$set": {"monto_total": total}}
        )

    def editar_pedido(self, pedido_id, pedido):
        self.pedidos.update_one(
            {"pedido_id": pedido_id},
            {"$set": pedido}
        )

    def eliminar_pedido(self, pedido_id):
        self.pedidos.delete_one(
            {"pedido_id": pedido_id}
        )


