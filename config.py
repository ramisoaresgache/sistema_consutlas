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
    "page_title": "Sistema de Consultas",
    "page_icon": "🔍",
    "layout": "wide"
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
    "header_title": "🔍 Sistema de Consultas",
    "welcome_message": "👋 <b>Hola {nombre}, que tengas un lindo día!</b>",
    "session_indicator": "🔒 Sesión persistente activa - Tu sesión se mantendrá al refrescar la página"
}

# Configuración de las pestañas
TABS_CONFIG = {
    "recibos": {
        "name": "📄 Consulta de Recibos",
        "header": "Consulta de Recibos por Comprobante",
        "description": "Ingresá los números de comprobante para buscar.",
    },
    "lotes": {
        "name": "🏦 Consulta de Lotes",
        "header": "Consulta el Lote",
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
        "name": "📄 Consulta de Declaraciones Juradas",
        "header": "Consulta de Declaraciones Juradas",
        "description": "Ingresá los criterios de búsqueda para las declaraciones juradas.",
    },
}

# Mensajes del sistema
MESSAGES = {
    "login": {
        "title": "🏢 Sistema de Consultas - Login",
        "subtitle": "Ingresá tus credenciales",
        "legajo_help": "Tu número de legajo personal",
        "password_help": "Por ahora, usá tu mismo número de legajo",
        "button_text": "🚀 Ingresar",
        "fields_required": "⚠️ Por favor completá todos los campos",
        "welcome": "✅ ¡Bienvenido/a {nombre}!",
        "credentials_error": "❌ Credenciales incorrectas. Verificá tu legajo y contraseña.",
        "unexpected_error": "❌ Error inesperado durante el login. Intentá nuevamente."
    },
    "session": {
        "restored": "🔄 Sesión restaurada automáticamente",
        "logout_button": "🚪 Cerrar Sesión"
    },
    "search": {
        "cancel_button": "🛑 Cancelar Búsqueda",
        "cancelled": "🛑 Búsqueda cancelada por el usuario",
        "no_results": "ℹ️ No se encontraron resultados para los criterios especificados.",
        "results_found": "✅ Se encontraron {count} resultados:",
        "download_button": "📥 Descargar resultados como CSV"
    },
    "validation": {
        "min_one_field": "⚠️ Debés ingresar al menos un criterio de búsqueda.",
        "min_one_comprobante": "⚠️ Ingresá al menos un número de comprobante válido."
    },
    "errors": {
        "database_error": "❌ Error al consultar la base de datos: {error}"
    }
}

# Configuración de consultas SQL
SQL_QUERIES = {
    "recibos": """
        SELECT c_sistema as sistema, n_comprob as comprobante, c_cuenta as cuenta, 
               c_tasa as tasa, n_ano as ano, n_cuota as cuota, 
               f_prim_vto as primer_vencimiento, i_deuda as importe, 
               i_rec_prim_vto as recargos, i_multa as multa 
        FROM recibos
        WHERE n_comprob IN ({placeholders})
    """,
    "lotes_bancarios": """
        SELECT n_archivo as numero_lote, n_comprob as comprobante, 
               f_cobro as fecha_cobro, c_cuenta as cuenta, 
               i_registro as importe, n_plan as numero_plan
        FROM bco_cab
        WHERE {where_clause}
    """,
    "cuenta_corriente": """
        SELECT t.c_sistema as sistema, t.n_transac as transaccion, 
               t.c_cuenta as cuenta, t.c_tasa as tasa, t.n_ano as ano, 
               t.n_cuota as cuota, c.c_estado_deuda as estado_deuda, 
               t.c_actual as estado_actual, c.n_comprob as comprobante, 
               c.n_orden as orden, c.f_pago as pago, 
               c.c_lugar_pago as lugar_pago, c.i_capital as importe, 
               c.i_recargo as recargo, c.i_multa as multa, 
               c.c_movimiento as movimiento  
        FROM transacciones t, cta_cte c
        WHERE {where_clause}
        AND t.n_transac = c.n_transac
    """,
    "declaraciones_juradas": """
        SELECT 
          a.c_id_ddjj AS ID_ddjj, 
          a.n_cuit AS cuit, 
          a.c_cuenta AS cuenta, 
          a.d_presentacion AS presentacion, 
          a.f_presentacion AS fecha_de_alta, 
          a.n_ano AS ano, 
          a.n_cuota AS cuota,  
          a.n_rub_act_prin AS rubro_principal, 
          a.c_baja AS baja, 
          a.id_simplificado AS id_simplificado
        FROM ddjj_sh_cab a
        WHERE {where_clause}
    """,
    "declaraciones_juradas_adicional": """
        SELECT 
          a.c_id_ddjj AS ID_ddjj, 
          a.n_cuit AS cuit, 
          a.c_cuenta AS cuenta, 
          a.d_presentacion AS presentacion, 
          a.f_presentacion AS fecha_de_alta, 
          b.f_baja_da AS fecha_de_baja,
          a.n_ano AS ano, 
          a.n_cuota AS cuota, 
          b.c_tasa_1 AS tasa, 
          a.n_rub_act_prin AS rubro_principal, 
          a.c_baja AS baja, 
          a.id_simplificado AS id_simplificado
        FROM ddjj_sh_cab a,regimen_simplificado_cuentas b, regimen_simplificado_cab c
        WHERE {where_clause}
        AND a.id_simplificado = b.id_simplificado
        AND a.id_simplificado = c.id_simplificado
    """,
    "usuario_login": "SELECT n_legajo, d_nombre FROM usuarios WHERE n_legajo = ? AND n_legajo = ?",
    "usuario_nombre": "SELECT d_nombre FROM usuarios WHERE n_legajo = ?",
}
