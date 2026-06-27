from pymongo import MongoClient

class bd:
    def __init__(self):
        self.cliente = MongoClient("mongodb://localhost:27017/")
        self.db = self.cliente["comerciotech"]
        self.clientes = self.db["clientes"]
        self.productos = self.db["productos"]
        self.pedidos = self.db["pedidos"]

    # CRUD CLIENTES

    def insertar_cliente(self, cliente):
        self.clientes.insert_one(cliente)

    def mostrar_clientes(self):
        return list(self.clientes.find())
    
    def actualizar_cliente(self, rut, direccion):
        self.clientes.update_one(
            {"rut": rut},
            {"$set": {"direccion": direccion}}
            )

    def eliminar_cliente(self, rut):
        self.clientes.delete_one(
            {"rut": rut}
            ) 
        
    # CRUD PRODUCTOS

    def insertar_producto(self, producto):
        self.productos.insert_one(producto)

    def mostrar_productos(self):
        return list(self.productos.find())
    
    def actualizar_stock(self, producto_id, stock):
        self.productos.update_one(
            {"_id": producto_id},
            {"$set": {"stock": stock}}
            )
        
    def eliminar_producto(self, producto_id):
        self.productos.delete_one(
            {"_id": producto_id}
            )
        
    # CRUD PEDIDOS

    def insertar_pedido(self, pedido):
        self.pedidos.insert_one(pedido)

    def mostrar_pedidos(self):
        return list(self.pedidos.find())

    def actualizar_total(self, pedido_id, total):
        self.pedidos.update_one(
            {"_id": pedido_id},
            {"$set": {"total": total}}
            )

    def eliminar_pedido(self, pedido_id):
        self.pedidos.delete_one(
            {"_id": pedido_id}
        )

        
