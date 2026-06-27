from bd import bd
from interfaz import ejecutar_interfaz

db = bd()

# Asegúrate de que aquí también se llame 'contrasenia'
def validar_login(usuario, contrasenia):
    return db.verificar_admin(usuario, contrasenia)

ejecutar_interfaz(validar_login, db)