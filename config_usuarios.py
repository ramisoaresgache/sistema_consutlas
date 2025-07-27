# Configuración de usuarios y roles del sistema
# Este archivo contiene la configuración de roles y permisos

# Definición de roles del sistema
ROLES = {
    'administrador': {
        'nombre': 'Administrador del Sistema',
        'permisos': [
            'consulta_recibos',
            'consulta_lotes', 
            'consulta_ctacte',
            'descargar_csv',
            'ver_queries',
            'administrar_usuarios',
            'ver_estadisticas',
            'exportar_reportes'
        ]
    },
    'consultor_senior': {
        'nombre': 'Consultor Senior',
        'permisos': [
            'consulta_recibos',
            'consulta_lotes',
            'consulta_ctacte', 
            'descargar_csv',
            'ver_queries',
            'ver_estadisticas'
        ]
    },
    'consultor_basico': {
        'nombre': 'Consultor Básico',
        'permisos': [
            'consulta_recibos',
            'consulta_lotes',
            'descargar_csv'
        ]
    },
    'solo_lectura': {
        'nombre': 'Solo Lectura',
        'permisos': [
            'consulta_recibos'
        ]
    }
}

# Asignación de roles por legajo (temporal - luego se moverá a la base de datos)
USUARIOS_ROLES = {
    # Ejemplo de asignaciones:
    # '1234': 'administrador',  # Rami (ejemplo)
    # '5678': 'consultor_senior',
    # '9999': 'consultor_basico',
    # Agregar más usuarios aquí según sea necesario
}

def obtener_rol_usuario(legajo):
    """Obtiene el rol de un usuario por su legajo"""
    return USUARIOS_ROLES.get(legajo, 'consultor_basico')  # Por defecto: consultor básico

def obtener_permisos_por_rol(rol):
    """Obtiene los permisos de un rol específico"""
    return ROLES.get(rol, {}).get('permisos', [])

def obtener_nombre_rol(rol):
    """Obtiene el nombre descriptivo de un rol"""
    return ROLES.get(rol, {}).get('nombre', 'Sin rol definido')
