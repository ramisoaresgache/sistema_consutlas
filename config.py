"""
Configuración del sistema de consultas
Centraliza todas las configuraciones y constantes
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página Streamlit
PAGE_CONFIG = {
    "page_title": "Sistema de la Municipalidad de Vicente López",
    "page_icon": "🏛",
    "layout": "wide",
}

# Configuración de conexión a la base de datos
DATABASE_CONFIG = {
    "conn_str": (
        f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
        f"HOST={os.getenv('DB_HOST')};"
        f"SERVICE={os.getenv('DB_SERVICE')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"PROTOCOL={os.getenv('DB_PROTOCOL')};"
        f"UID={os.getenv('DB_UID')};"
        f"PWD={os.getenv('DB_PWD')};"
    )
}

# Configuración de la interfaz
UI_CONFIG = {
    "header_title": "🏛 Sistema de la Municipalidad de Vicente López",
    "welcome_message": "👋 <b>Hola {nombre}, que tengas un lindo día!</b>",
    "session_indicator": "🔒 Sesión persistente activa - Tu sesión se mantendrá al refrescar la página",
}

# Configuración de las pestañas
TABS_CONFIG = {
    "recibos": {
        "name": "📄 Consulta de Recibos",
        "header": "Consulta de Recibos por Comprobante",
        "description": "Ingresá los números de comprobante para buscar.",
    },
    "lotes": {
        "name": "🏦 Consulta de Lotes y Cajas",
        "header": "Consulta el Lote o la Caja",
        "description": "Podés filtrar por uno o más campos. Dejá en blanco los campos que no querés usar como filtro.",
    },
    "cuenta_corriente": {
        "name": "💳 Consulta de Cta Cte",
        "header": "Consulta de Cuenta Corriente",
        "description": "Consultá cuenta corriente. Podés filtrar por uno o más campos.",
    },
    "generador_reportes": {
        "name": "📊 Generador de Reportes",
        "header": "Generador de Reportes Visual",
        "description": "Creá tus propios reportes personalizados sin necesidad de conocimiento técnico.",
    },
    "declaraciones_juradas": {
        "name": "👨🏼‍⚖️ Consulta de Declaraciones Juradas",
        "header": "Consulta de Declaraciones Juradas",
        "description": "Ingresá los criterios de búsqueda para las declaraciones juradas.",
    },
    "planes": {
        "name": "📒 Consulta de Planes",
        "header": "Consulta de Planes de Pago",
        "description": "Ingresá el número de plan para consultar la información detallada.",
    },
    "debitos_automaticos": {
        "name": "🏦 Consulta de Débitos Automáticos",
        "header": "Consulta de Débitos Automáticos",
        "description": "Consultá débitos automáticos de ABL y PPC ePagos. Podés filtrar por uno o más campos.",
    },
}

# Mensajes del sistema
MESSAGES = {
    "login": {
        "title": "🏛 Sistema de Consultas - Login",
        "subtitle": "Ingresá tus credenciales",
        "legajo_help": "Tu número de legajo personal",
        "password_help": "Por ahora, usá tu mismo número de legajo",
        "button_text": "🚀 Ingresar",
        "fields_required": "⚠️ Por favor completá todos los campos",
        "welcome": "✅ ¡Bienvenido/a {nombre}!",
        "credentials_error": "❌ Credenciales incorrectas. Verificá tu legajo y contraseña.",
        "unexpected_error": "❌ Error inesperado durante el login. Intentá nuevamente.",
        "logo_path": os.path.join(
            os.path.dirname(__file__), "imagenes", "descarga.jpeg"
        ),
    },
    "session": {
        "restored": "🔄 Sesión restaurada automáticamente",
        "logout_button": "🚪 Cerrar Sesión",
    },
    "search": {
        "cancel_button": "🛑 Cancelar Búsqueda",
        "cancelled": "🛑 Búsqueda cancelada por el usuario",
        "no_results": "ℹ️ No se encontraron resultados para los criterios especificados.",
        "results_found": "✅ Se encontraron {count} resultados:",
        "download_button": "📥 Descargar resultados como Excel",
        "limit_info": "ℹ️ Las consultas están limitadas a 1000 registros para optimizar el rendimiento.",
    },
    "validation": {
        "min_one_field": "⚠️ Debés ingresar al menos un criterio de búsqueda.",
        "min_one_comprobante": "⚠️ Ingresá al menos un número de comprobante válido.",
    },
    "errors": {"database_error": "❌ Error al consultar la base de datos: {error}"},
}
 
