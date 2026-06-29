from bd import bd
from interfaz import ejecutar_interfaz

db = bd()

def validar_login(usuario, contrasenia):
    usuario = usuario.strip()
    contrasenia = contrasenia.strip()
    if not usuario:
        return "user_not_found"
    if not contrasenia:
        return "wrong_password"
    if db.verificar_admin(usuario, contrasenia):
        return "ok"
    if usuario != db.usuario:
        return "user_not_found"
    return "wrong_password"

ejecutar_interfaz(validar_login, db)