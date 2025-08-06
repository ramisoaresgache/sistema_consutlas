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
        SELECT d_sub_cod as sistema, n_comprob as comprobante, c_cuenta as cuenta, 
               c_tasa as tasa, n_ano as ano, n_cuota as cuota, 
               f_prim_vto as primer_vencimiento, i_deuda as importe, 
               i_rec_prim_vto as recargos, i_multa as multa 
        FROM recibos, codificaciones 
        WHERE n_comprob IN ({placeholders})
        AND codificaciones.c_codificacion = 11
        AND codificaciones.c_sub_cod = recibos.c_sistema
    """,
    "lotes_bancarios": """
SELECT 
	a.n_archivo as numero_lote, 
case 
	when b.c_estado = 5 then "ACTUALIZADO" 
	when b.c_estado = 2 then "PROCESASDO" 
	when b.c_estado = 6 then "ANULADO" 
end as estado,
	a.n_comprob as comprobante, 
	a.f_cobro as fecha_cobro, a.c_cuenta as cuenta, 
	a.i_registro as importe, a.n_plan as numero_plan
FROM bco_cab a, bco_archivos b
WHERE a.n_archivo = b.n_archivo
and {where_clause}
    """,
    "cuenta_corriente": """
        SELECT d.d_sub_cod as sistema, t.n_transac as transaccion, 
               t.c_cuenta as cuenta, s.d_tasa as tasa, t.n_ano as ano, 
               t.n_cuota as cuota, c.c_estado_deuda as estado_deuda, 
               t.c_actual as estado_actual, c.n_comprob as comprobante, 
               c.n_orden as orden, c.f_pago as pago, 
               e.d_lugar_pago as lugar_pago, c.i_capital as importe, 
               c.i_recargo as recargo, c.i_multa as multa, 
               c.c_movimiento as movimiento  
        FROM transacciones t
        INNER JOIN cta_cte c ON t.n_transac = c.n_transac
        JOIN codificaciones d ON t.c_sistema = d.c_sub_cod
        LEFT JOIN estadisticas_lugares_de_pago e ON c.c_lugar_pago = e.c_lugar_pago
        JOIN tasas s ON t.c_tasa = s.c_tasa
        WHERE {where_clause}
        AND d.c_codificacion = 11
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
        WHERE a.n_rub_act_prin = c.c_rubro
        AND {where_clause}
        ORDER BY a.n_ano DESC
            """,
    "declaraciones_juradas_adicional": """
SELECT unique
          a.n_cuit AS cuit, 
          a.c_cuenta AS cuenta, 
          a.d_presentacion AS presentacion, 
          a.f_presentacion AS fecha_de_alta, 
          a.n_ano AS ano, 
          a.n_cuota AS cuota, 
          d.d_tasa AS tasa, 
          c.d_rub_act as actividad,
          b.n_personas AS cantidad_personas,
          b.i_imponible AS imponible_tasa,
        CASE 
            WHEN a.c_baja = 1 THEN 'BAJA' 
            WHEN a.c_baja = 0 THEN 'ACTIVA' 
            ELSE 'SIN DATOS'
        END AS baja
        FROM ddjj_sh_cab a, ddjj_sh_det b, rubro_actividad_rel c, tasas d
        WHERE {where_clause}
        AND a.c_id_ddjj = b.c_id_ddjj
        AND a.n_rub_act_prin = c.c_rubro
        AND b.c_tasa = d.c_tasa
        ORDER BY a.n_ano DESC, a.n_cuota DESC
        """,
    "declaraciones_juradas_detalle_simplificado": """
        SELECT unique
          a.n_ano AS ano, 
          a.n_cuota AS cuota, 
          c.d_rub_act as actividad,
          d.d_tasa AS tasa, 
          b.i_imponible AS imponible_tasa,
        CASE
            when e.c_pyp1 > 0 then "SI"
            when e.c_pyp1 = 0 then "NO"
        END AS cartel1,
        CASE
            when e.c_pyp2 > 0 then "SI"
            when e.c_pyp2 = 0 then "NO"
        END AS cartel2,
        CASE
            when e.c_pyp3 > 0 then "SI"
            when e.c_pyp3 = 0 then "NO"
        END AS cartel3,
        CASE
            when e.c_pyp4 > 0 then "SI"
            when e.c_pyp4 = 0 then "NO"
        END AS cartel4,
        CASE
            when e.c_pyp5 > 0 then "SI"
            when e.c_pyp5 = 0 then "NO"
        END AS cartel5,
        CASE
            when e.c_pyp6 > 0 then "SI"
            when e.c_pyp6 = 0 then "NO"
        END AS cartel6,
        CASE
            when e.c_pyp7 > 0 then "SI"
            when e.c_pyp7 = 0 then "NO"
        END AS cartel7,
        CASE
            when e.c_pyp8 > 0 then "SI"
            when e.c_pyp8 = 0 then "NO"
        END AS cartel8,
        CASE
            when e.c_pyp9 > 0 then "SI"
            when e.c_pyp9 = 0 then "NO"
        END AS cartel9,
        CASE
            when e.c_pyp10 > 0 then "SI"
            when e.c_pyp10 = 0 then "NO"
        END AS cartel10,
        CASE
            when e.c_oep1 > 0 then "SI"
            when e.c_oep1 = 0 then "NO"
        END AS espacios_publicos1,
        CASE
            when e.c_oep2 > 0 then "SI"
            when e.c_oep2 = 0 then "NO"
        END AS espacios_publicos2,
        CASE
            when e.c_sv1 > 0 then "SI"
            when e.c_sv1 = 0 then "NO"
        END AS seguridad_vial1,
        CASE
            when e.c_sv2 > 0 then "SI"
            when e.c_sv2 = 0 then "NO"
        END AS seguridad_vial2
        FROM ddjj_sh_cab a, ddjj_sh_det b, rubro_actividad_rel c, tasas d, tmp_graba_datos_cab e--, transacciones f
        WHERE a.c_id_ddjj = b.c_id_ddjj
        --and b.n_transac = f.n_transac
        --and b.i_imponible = e.i_imponible
        AND a.c_cuenta = e.c_cuenta 
        AND a.n_cuit = e.n_cuit 
        AND a.n_rub_act_prin = c.c_rubro
        AND b.c_tasa = d.c_tasa
        AND {where_clause}
        ORDER BY a.n_ano DESC
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
        AND c.c_codificacion = 36
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
            c.d_sub_cod as sistema,
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
        FROM per_cuotas_ppc a, transacciones b, codificaciones c
        WHERE a.n_transac = b.n_transac 
        AND c.c_codificacion = 11
        AND b.c_sistema = c.c_sub_cod
        AND {where_clause}
    ""","debitos_abl": """
    SELECT 
            b.d_sub_cod,
            a.c_cuenta AS cuenta, 
            a.c_tasa as tasa,
            a.f_alta AS alta_debito,
    CASE 
        WHEN a.f_baja > TODAY THEN 'activo'
        WHEN a.f_baja <= TODAY THEN TO_CHAR(a.f_baja, '%Y-%m-%d') 
    END AS baja_debito
    FROM debitos a, codificaciones b 
    WHERE {where_clause}
    AND a.c_banco = b.c_sub_cod 
    AND b.c_codificacion = 37  
""","debitos_ppc_epagos": """
    select distinct
        a.n_plan as plan, 
        b.n_cuit as cuit, 
        b.f_alta as fecha_alta, 
        b.f_baja as fecha_baja, 
    case
        when a.c_estado = "FIN" then "FINALIZADO" 
        when a.c_estado = "PEN" then "PENDIENTE" 
    end as estado
    from ppc_epagos_debito_directo_estado a, ppc_epagos_debito_directo_registrados b
    where a.n_plan = b.n_plan 
    and a.n_plan {where_clause}
""",
    "usuario_login": "SELECT n_legajo, d_nombre FROM usuarios WHERE n_legajo = ? AND n_legajo = ?",
    "usuario_nombre": "SELECT d_nombre FROM usuarios WHERE n_legajo = ?",
}
