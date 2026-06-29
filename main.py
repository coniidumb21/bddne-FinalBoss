from bd import bd
from interfaz import ejecutar_interfaz

db = bd()

def validar_login(usuario, contrasenia):
    usuario = usuario.strip()
    contrasenia = contrasenia.strip()
    admin = db.buscar_admin_por_usuario(usuario)
    if admin is None:
        return "user_not_found"
    if admin.get("contrasenia") != contrasenia:
        return "wrong_password"
    return "ok"

ejecutar_interfaz(validar_login, db)