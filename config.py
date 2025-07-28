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
    "planes": {
        "name": "📋 Consulta de Planes",
        "header": "Consulta de Planes de Pago",
        "description": "Ingresá el número de plan para consultar la información detallada.",
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
        # Ejemplo de cómo agregar una imagen local (usando Streamlit):
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
        FROM transacciones t 
        INNER JOIN cta_cte c ON t.n_transac = c.n_transac
        WHERE {where_clause}
        ORDER BY t.c_sistema, t.n_transac,t.n_ano, t.n_cuota, c.n_orden
    """,
    "declaraciones_juradas": """
       SELECT 
          a.n_cuit AS cuit, 
          a.c_cuenta AS cuenta,
          a.d_contacto AS contacto,
          a.d_mail_contacto AS email_contacto,
          a.d_tel_contacto AS telefono_contacto, 
          a.d_presentacion AS presentacion, 
          a.f_presentacion AS fecha_de_alta, 
          a.n_ano AS ano, 
          a.n_cuota AS cuota, 
          c.d_rub_act as actividad_principal,
        CASE 
            WHEN a.c_baja = 1 THEN 'BAJA' 
            WHEN a.c_baja = 0 THEN 'ACTIVA' 
            ELSE 'SIN DATOS'
        END AS baja
        FROM ddjj_sh_cab a, rubro_actividad_rel c
        where a.n_rub_act_prin = c.n_rub_act
        and {where_clause}
        order by a.n_ano desc
            """,
    "declaraciones_juradas_adicional": """
SELECT 
          a.c_id_ddjj AS ID_ddjj, 
          a.n_cuit AS cuit, 
          a.c_cuenta AS cuenta, 
          a.d_presentacion AS presentacion, 
          a.f_presentacion AS fecha_de_alta, 
          a.n_ano AS ano, 
          a.n_cuota AS cuota, 
          b.c_tasa_1 AS tasa, 
          c.d_rub_act as actividad,
        CASE 
            WHEN a.c_baja = 1 THEN 'SI' 
            WHEN a.c_baja = 0 THEN 'NO' 
            ELSE 'SIN DATOS'
        END AS baja,
          a.id_simplificado AS id_simplificado
        FROM ddjj_sh_cab a, regimen_simplificado_cuentas b, rubro_actividad_rel c
        WHERE {where_clause}
        AND a.id_simplificado = b.id_simplificado
        AND a.n_rub_act_prin = c.c_rubro
        """,
    "planes": """
        SELECT 
            a.n_plan AS plan,
            a.n_cant_cuotas AS cantidad_cuotas,
            a.n_porc_ant AS porcentaje_anticipo,
            a.i_anticipo AS importe_anticipo,
            c.d_sub_cod AS estado,
            SUM(b.i_capital + b.i_recargo + b.i_multa) AS total_plan
        FROM ppc_cab a
        JOIN per_cuotas_ppc b ON a.n_plan = b.n_plan join codificaciones c on  a.c_estado = c.c_sub_cod
        WHERE {where_clause}
        and c.c_codificacion = 36
        GROUP BY 1,2,3,4,5
    """,
    "planes_consulta_cuotas": """
        SELECT 
          a.n_plan as plan,
          b.n_cuota_plan as cuota_plan,
          b.f_vencimiento as fecha_vencimiento,
          b.i_capital as capital_cuota,
          b.i_recargo as recargos_cuotas,
          b.i_interes_fin as intereses_cuota,
          b.i_multa as multa,
          b.f_pago as fecha_pago_cuota
        FROM ppc_cab a, cuotas_ppc b
        WHERE a.n_plan = b.n_plan
        AND {where_clause}
        ORDER BY a.n_plan, b.n_cuota_plan
    """,
    "planes_transacciones": """
   SELECT 
       b.c_sistema as sistema,
       a.n_plan as plan, 
       a.n_cuota_plan as cuota_plan,
       b.c_cuenta as cuenta,
       b.c_tasa as tasa,
       b.n_ano as ano,
       b.n_cuota as cuota_periodo,
       b.c_actual as estado,
       a.i_capital as capital,
       a.i_recargo as recargo,
       a.i_multa as multa
       FROM per_cuotas_ppc a, transacciones b
       WHERE a.n_transac = b.n_transac 
       AND {where_clause}
    """,
    "usuario_login": "SELECT n_legajo, d_nombre FROM usuarios WHERE n_legajo = ? AND n_legajo = ?",
    "usuario_nombre": "SELECT d_nombre FROM usuarios WHERE n_legajo = ?",
}
