# Sistema de permisos por usuarios
# Este archivo define los permisos que cada usuario puede tener

import streamlit as st
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de conexión (igual que en el archivo principal)
conn_str = (
    f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
    f"HOST={os.getenv('DB_HOST')};"
    f"SERVICE={os.getenv('DB_SERVICE')};"
    f"DATABASE={os.getenv('DB_DATABASE')};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"PROTOCOL={os.getenv('DB_PROTOCOL')};"
    f"UID={os.getenv('DB_UID')};"
    f"PWD={os.getenv('DB_PWD')};"
)

class PermisosSistema:
    """Clase para manejar permisos de usuarios"""
    
    def __init__(self):
        # Definir permisos disponibles
        self.permisos_disponibles = {
            'consulta_recibos': 'Consultar tabla de recibos',
            'consulta_lotes': 'Consultar tabla de lotes bancarios', 
            'consulta_ctacte': 'Consultar cuenta corriente',
            'descargar_csv': 'Descargar resultados en CSV',
            'ver_queries': 'Ver queries SQL generadas',
            'administrar_usuarios': 'Administrar otros usuarios'
        }
    
    def obtener_permisos_usuario(self, legajo):
        """
        Obtiene los permisos de un usuario desde la base de datos
        Por ahora, todos los usuarios tienen todos los permisos
        Más adelante se puede agregar una tabla de permisos
        """
        try:
            # TODO: Implementar tabla de permisos en el futuro
            # Por ahora, todos tienen acceso completo excepto administración
            permisos_default = {
                'consulta_recibos': True,
                'consulta_lotes': True,
                'consulta_ctacte': True,
                'descargar_csv': True,
                'ver_queries': True,
                'administrar_usuarios': False  # Solo algunos usuarios específicos
            }
            
            # Usuarios administradores (ejemplo)
            admins = ['37329']  # Legajos de administradores
            if legajo in admins:
                permisos_default['administrar_usuarios'] = True
            
            return permisos_default
            
        except Exception as e:
            st.error(f"Error al obtener permisos: {e}")
            return {}
    
    def verificar_permiso(self, permiso):
        """Verifica si el usuario actual tiene un permiso específico"""
        if 'user_legajo' not in st.session_state:
            return False
        
        if 'user_permisos' not in st.session_state:
            st.session_state.user_permisos = self.obtener_permisos_usuario(
                st.session_state.user_legajo
            )
        
        return st.session_state.user_permisos.get(permiso, False)
    
    def mostrar_pestana_si_tiene_permiso(self, permiso, contenido_pestana):
        """Muestra el contenido de una pestaña solo si el usuario tiene permiso"""
        if self.verificar_permiso(permiso):
            return contenido_pestana
        else:
            st.warning(f"🚫 No tenés permisos para acceder a esta sección.")
            st.info("Contactá al administrador si necesitás acceso.")
            return None

# Función de utilidad para verificar permisos
def tiene_permiso(permiso):
    """Función rápida para verificar permisos"""
    permisos = PermisosSistema()
    return permisos.verificar_permiso(permiso)

# Ejemplo de uso futuro:
"""
# En el archivo principal, podrías usar así:

if tiene_permiso('consulta_recibos'):
    # Mostrar pestaña de recibos
    with tab1:
        # ... código de consulta recibos
else:
    st.warning("No tenés permiso para consultar recibos")

if tiene_permiso('descargar_csv'):
    st.download_button(...)  # Mostrar botón de descarga
"""
