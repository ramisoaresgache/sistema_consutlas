"""
Control de acceso - Lista de usuarios autorizados
Este archivo contiene la lista de legajos que pueden acceder al sistema
"""

# Lista de usuarios autorizados (legajos)
# Solo los usuarios en esta lista podrán ingresar al sistema
USUARIOS_AUTORIZADOS = [
  37329
]

# Configuración del control de acceso
CONFIGURACION_ACCESO = {
    'mensaje_acceso_denegado': "🚫 No tenés autorización para acceder a este sistema. Contactá al administrador.",
    'mostrar_legajo_en_error': True,  # Si mostrar el legajo en el mensaje de error
    'log_intentos_fallidos': True    # Si registrar intentos de acceso fallidos
}

def esta_autorizado(legajo):
    """
    Verifica si un legajo está en la lista de autorizados
    
    Args:
        legajo (str o int): El legajo a verificar
    
    Returns:
        bool: True si está autorizado, False si no
    """
    try:
        legajo_int = int(legajo)
        return legajo_int in USUARIOS_AUTORIZADOS
    except (ValueError, TypeError):
        return False

def mostrar_usuarios_autorizados():
    """
    Devuelve la lista de usuarios autorizados para mostrar
    """
    return USUARIOS_AUTORIZADOS.copy()

def agregar_usuario_autorizado(legajo):
    """
    Agrega un usuario a la lista de autorizados (temporal - solo en memoria)
    Para cambios permanentes, editá este archivo
    
    Args:
        legajo (str o int): El legajo a agregar
    
    Returns:
        bool: True si se agregó exitosamente
    """
    try:
        legajo_int = int(legajo)
        if legajo_int not in USUARIOS_AUTORIZADOS:
            USUARIOS_AUTORIZADOS.append(legajo_int)
            return True
        return False
    except (ValueError, TypeError):
        return False

def quitar_usuario_autorizado(legajo):
    """
    Quita un usuario de la lista de autorizados (temporal - solo en memoria)
    Para cambios permanentes, editá este archivo
    
    Args:
        legajo (str o int): El legajo a quitar
    
    Returns:
        bool: True si se quitó exitosamente
    """
    try:
        legajo_int = int(legajo)
        if legajo_int in USUARIOS_AUTORIZADOS:
            USUARIOS_AUTORIZADOS.remove(legajo_int)
            return True
        return False
    except (ValueError, TypeError):
        return False

def contar_usuarios_autorizados():
    """
    Devuelve la cantidad de usuarios autorizados
    """
    return len(USUARIOS_AUTORIZADOS)

# Información para el administrador
print(f"📋 Control de acceso cargado: {contar_usuarios_autorizados()} usuarios autorizados")
