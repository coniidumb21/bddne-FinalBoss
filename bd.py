import datetime
import json
import os
import subprocess

from cryptography.fernet import Fernet
from pymongo import MongoClient

class bd:
    KEY_FILE = "secret.key"
    CREDENTIALS_FILE = "credentials.enc"

    def __init__(self):
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.key_path = os.path.join(self.base_path, self.KEY_FILE)
        self.credentials_path = os.path.join(self.base_path, self.CREDENTIALS_FILE)
        self.key = self._load_or_create_key()
        self.usuario, self.contrasenia = self._load_or_create_credentials()
        self.uri = f"mongodb://{self.usuario}:{self.contrasenia}@localhost:27017/?authSource=admin"
        self.cliente = MongoClient(self.uri)
        self.db = self.cliente["comercioTech"]
        self.admin = self.db["admin"]
        self.clientes = self.db["clientes"]
        self.productos = self.db["productos"]
        self.pedidos = self.db["pedidos"]

    def _load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                return key_file.read()
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as key_file:
            key_file.write(key)
        return key

    def _encrypt_text(self, texto):
        f = Fernet(self.key)
        return f.encrypt(texto.encode()).decode()

    def _decrypt_text(self, texto_encriptado):
        f = Fernet(self.key)
        return f.decrypt(texto_encriptado.encode()).decode()

    def _load_or_create_credentials(self):
        if os.path.exists(self.credentials_path):
            with open(self.credentials_path, "r", encoding="utf-8") as cred_file:
                data = json.load(cred_file)
            return (
                self._decrypt_text(data["usuario"]),
                self._decrypt_text(data["contrasenia"]),
            )

        default_usuario = "administrador"
        default_contrasenia = "123456"
        data = {
            "usuario": self._encrypt_text(default_usuario),
            "contrasenia": self._encrypt_text(default_contrasenia),
        }
        with open(self.credentials_path, "w", encoding="utf-8") as cred_file:
            json.dump(data, cred_file)
        return default_usuario, default_contrasenia

    # Verificar Admin
    def buscar_admin_por_usuario(self, usuario):
        return self.db["admin"].find_one({"usuario": usuario})

    def verificar_admin(self, usuario, contrasenia):
        uri = f"mongodb://{usuario}:{contrasenia}@localhost:27017/?authSource=admin"
        try:
            cliente_temporal = MongoClient(uri, serverSelectionTimeoutMS=3000)
            cliente_temporal.admin.command("ping")
            return True
        except Exception:
            return False

    def respaldar_datos(self, destino=None):
        if destino is None:
            backup_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), "backups")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            destino = os.path.join(backup_root, f"backup_{timestamp}")

        os.makedirs(destino, exist_ok=True)

        try:
            subprocess.run(
                ["mongodump", "--uri", self.uri, "--out", destino],
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as err:
            raise RuntimeError(
                "mongodump no está disponible. Instala MongoDB Database Tools y asegúrate de que mongodump esté en el PATH."
            ) from err
        except subprocess.CalledProcessError as err:
            raise RuntimeError(
                f"Error durante mongodump: {err.stderr.strip() if err.stderr else err}"
            ) from err

        return destino
            
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


