"""
Módulo de consultas SQL (builders)
Contiene la clase SQLBuilder con generadores de SQL reutilizables.
"""


class SQLBuilder:
    """Generador de consultas SQL dinámicas."""

    @staticmethod
    def recibos(placeholders: str) -> str:
        return f"""
SELECT d_sub_cod AS sistema, n_comprob AS comprobante, c_cuenta AS cuenta,
    c_tasa AS tasa, n_ano AS ano, n_cuota AS cuota,
    f_prim_vto AS primer_vencimiento, i_deuda AS importe,
    i_rec_prim_vto AS recargos, i_multa AS multa
FROM recibos, codificaciones
WHERE n_comprob IN ({placeholders})
AND codificaciones.c_codificacion = 11
AND codificaciones.c_sub_cod = recibos.c_sistema
"""
    @staticmethod
    def consulta_cajas(where_clause: str) -> str:
        return f"""
SELECT 
    n_apertura AS numero_apertura,
    n_transac AS numero_transaccion,
    n_comprob AS numero_comprobante,
    f_cobro AS fecha_cobro
FROM cobros_cajas
WHERE {where_clause}
"""
    @staticmethod
    def lotes_bancarios(where_clause: str) -> str:
        return f"""
SELECT 
    a.n_archivo AS numero_lote, 
CASE 
    WHEN b.c_estado = 5 THEN "ACTUALIZADO"
    WHEN b.c_estado = 2 THEN "PROCESADO"
    WHEN b.c_estado = 6 THEN "ANULADO"
END AS estado,
    a.n_comprob AS comprobante,
    a.f_cobro AS fecha_cobro, a.c_cuenta AS cuenta,
    a.i_registro AS importe, a.n_plan AS numero_plan
FROM bco_cab a, bco_archivos b
WHERE a.n_archivo = b.n_archivo
AND {where_clause}
"""

    @staticmethod
    def cuenta_corriente(where_clause: str) -> str:
        return f"""
SELECT d.d_sub_cod AS sistema, t.n_transac AS transaccion, 
    t.c_cuenta AS cuenta, s.d_tasa AS tasa, t.n_ano AS ano, 
    t.n_cuota AS cuota, c.c_estado_deuda AS estado_deuda, 
    t.c_actual AS estado_actual, c.n_comprob AS comprobante, 
    c.n_orden AS orden, c.f_pago AS pago, 
    e.d_lugar_pago AS lugar_pago, c.i_capital AS importe, 
    c.i_recargo AS recargo, c.i_multa AS multa, 
    c.c_movimiento AS movimiento  
FROM transacciones t
INNER JOIN cta_cte c ON t.n_transac = c.n_transac
JOIN codificaciones d ON t.c_sistema = d.c_sub_cod
LEFT JOIN estadisticas_lugares_de_pago e ON c.c_lugar_pago = e.c_lugar_pago
JOIN tasas s ON t.c_tasa = s.c_tasa
WHERE {where_clause}
AND d.c_codificacion = 11
ORDER BY t.c_sistema, t.n_transac,t.n_ano, t.n_cuota, c.n_orden
"""

    @staticmethod
    def declaraciones_juradas(where_clause: str) -> str:
        return f"""
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
    c.d_rub_act AS actividad_principal,
CASE 
    WHEN a.c_baja = 1 THEN 'BAJA' 
    WHEN a.c_baja = 0 THEN 'ACTIVA' 
    ELSE 'SIN DATOS'
END AS baja
FROM ddjj_sh_cab a, rubro_actividad_rel c
WHERE a.n_rub_act_prin = c.c_rubro
AND {where_clause}
ORDER BY a.n_ano DESC
"""

    @staticmethod
    def declaraciones_juradas_adicional(where_clause: str) -> str:
        return f"""
SELECT unique
    a.n_cuit AS cuit, 
    a.c_cuenta AS cuenta, 
    a.d_presentacion AS presentacion, 
    a.f_presentacion AS fecha_de_alta, 
    a.n_ano AS ano, 
    a.n_cuota AS cuota, 
    d.d_tasa AS tasa, 
    c.d_rub_act AS actividad,
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
"""

    @staticmethod
    def declaraciones_juradas_detalle_simplificado(where_clause: str) -> str:
        return f"""
SELECT unique
    a.n_ano AS ano, 
    a.n_cuota AS cuota, 
    c.d_rub_act as actividad,
    d.d_tasa AS tasa, 
    b.i_imponible AS imponible_tasa,
CASE
    WHEN e.c_pyp1 > 0 THEN "SI"
    WHEN e.c_pyp1 = 0 THEN "NO"
END AS cartel1,
CASE
    WHEN e.c_pyp2 > 0 THEN "SI"
    WHEN e.c_pyp2 = 0 THEN "NO"
END AS cartel2,
CASE
    WHEN e.c_pyp3 > 0 THEN "SI"
    WHEN e.c_pyp3 = 0 THEN "NO"
END AS cartel3,
CASE
    WHEN e.c_pyp4 > 0 THEN "SI"
    WHEN e.c_pyp4 = 0 THEN "NO"
END AS cartel4,
CASE
    WHEN e.c_pyp5 > 0 THEN "SI"
    WHEN e.c_pyp5 = 0 THEN "NO"
END AS cartel5,
CASE
    WHEN e.c_pyp6 > 0 THEN "SI"
    WHEN e.c_pyp6 = 0 THEN "NO"
END AS cartel6,
CASE
    WHEN e.c_pyp7 > 0 THEN "SI"
    WHEN e.c_pyp7 = 0 THEN "NO"
END AS cartel7,
CASE
    WHEN e.c_pyp8 > 0 THEN "SI"
    WHEN e.c_pyp8 = 0 THEN "NO"
END AS cartel8,
CASE
    WHEN e.c_pyp9 > 0 THEN "SI"
    WHEN e.c_pyp9 = 0 THEN "NO"
END AS cartel9,
CASE
    WHEN e.c_pyp10 > 0 THEN "SI"
    WHEN e.c_pyp10 = 0 THEN "NO"
END AS cartel10,
CASE
    WHEN e.c_oep1 > 0 THEN "SI"
    WHEN e.c_oep1 = 0 THEN "NO"
END AS espacios_publicos1,
CASE
    WHEN e.c_oep2 > 0 THEN "SI"
    WHEN e.c_oep2 = 0 THEN "NO"
END AS espacios_publicos2,
CASE
    WHEN e.c_sv1 > 0 THEN "SI"
    WHEN e.c_sv1 = 0 THEN "NO"
END AS seguridad_vial1,
CASE
    WHEN e.c_sv2 > 0 THEN "SI"
    WHEN e.c_sv2 = 0 THEN "NO"
END AS seguridad_vial2
FROM ddjj_sh_cab a, ddjj_sh_det b, rubro_actividad_rel c, tasas d, tmp_graba_datos_cab e
WHERE a.c_id_ddjj = b.c_id_ddjj
AND a.c_cuenta = e.c_cuenta 
AND a.n_cuit = e.n_cuit 
AND a.n_rub_act_prin = c.c_rubro
AND b.c_tasa = d.c_tasa
AND {where_clause}
ORDER BY a.n_ano DESC
"""

    @staticmethod
    def planes(where_clause: str) -> str:
        return f"""
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
"""

    @staticmethod
    def planes_consulta_cuotas(where_clause: str) -> str:
        return f"""
SELECT 
    a.n_plan AS plan,
    b.n_cuota_plan AS cuota_plan,
    b.f_vencimiento AS fecha_vencimiento,
    b.i_capital AS capital_cuota,
    b.i_recargo AS recargos_cuotas,
    b.i_interes_fin AS intereses_cuota,
    b.i_multa AS multa,
    b.f_pago AS fecha_pago_cuota
FROM ppc_cab a, cuotas_ppc b
WHERE a.n_plan = b.n_plan
AND {where_clause}
ORDER BY a.n_plan, b.n_cuota_plan
"""

    @staticmethod
    def planes_transacciones(where_clause: str) -> str:
        return f"""
SELECT 
    c.d_sub_cod AS sistema,
    a.n_plan AS plan, 
    a.n_cuota_plan AS cuota_plan,
    b.c_cuenta AS cuenta,
    b.c_tasa AS tasa,
    b.n_ano AS ano,
    b.n_cuota AS cuota_periodo,
    b.c_actual AS estado,
    a.i_capital AS capital,
    a.i_recargo AS recargo,
    a.i_multa AS multa
FROM per_cuotas_ppc a, transacciones b, codificaciones c
WHERE a.n_transac = b.n_transac 
AND c.c_codificacion = 11
AND b.c_sistema = c.c_sub_cod
AND {where_clause}
"""

    @staticmethod
    def debitos_abl(where_clause: str) -> str:
        return f"""
SELECT 
        b.d_sub_cod,
        a.c_cuenta AS cuenta, 
        a.c_tasa as tasa,
        a.f_alta AS alta_debito,
        a.f_baja AS fecha_baja,
CASE 
    WHEN a.f_baja > TODAY THEN 'activo'
    WHEN a.f_baja <= TODAY THEN TO_CHAR(a.f_baja, '%Y-%m-%d') 
END AS estado
FROM debitos a, codificaciones b 
WHERE {where_clause}
AND a.c_banco = b.c_sub_cod 
AND b.c_codificacion = 37  
"""

    @staticmethod
    def debitos_ppc_epagos(where_clause: str) -> str:
        return f"""
SELECT DISTINCT
    a.n_plan AS plan, 
    b.n_cuit AS cuit, 
    b.f_alta AS fecha_alta, 
    b.f_baja AS fecha_baja, 
CASE
    WHEN a.c_estado = "FIN" THEN "FINALIZADO" 
    WHEN a.c_estado = "PEN" THEN "PENDIENTE" 
END AS estado
FROM ppc_epagos_debito_directo_estado a, ppc_epagos_debito_directo_registrados b
WHERE a.n_plan = b.n_plan 
AND a.n_plan {where_clause}
"""

    # --- Reportes estadísticos ---
    @staticmethod
    def estadisticas_deuda_base(ano: int, cuota: int) -> str:
        return f"""
WITH deuda_total AS (
  SELECT 
    a.c_sistema, a.n_transac, a.c_cuenta, a.c_tasa, a.n_ano, a.n_cuota, a.c_actual,
    b.n_comprob, b.c_lugar_pago, b.i_capital, b.i_recargo, b.i_multa, b.c_movimiento
  FROM transacciones a
  JOIN cta_cte b ON a.n_transac = b.n_transac
  WHERE a.n_ano = ? AND a.n_cuota = ? 
    AND b.n_orden = 1 
    AND b.c_movimiento IN (207, 249)
)
SELECT 
  a.c_sistema, a.c_cuenta, a.c_tasa, a.n_ano, a.n_cuota,
  b.n_comprob, b.c_movimiento,
  SUM(COALESCE(b.i_capital,0)+COALESCE(b.i_recargo,0)+COALESCE(b.i_multa,0)) AS total
FROM deuda_total a
JOIN cta_cte b ON a.n_transac = b.n_transac
JOIN transacciones c ON b.n_transac = c.n_transac
WHERE b.n_orden > 1 AND b.c_movimiento = 74
GROUP BY 
  a.c_sistema, a.c_cuenta, a.c_tasa, a.n_ano, a.n_cuota, b.n_comprob, b.c_movimiento;
"""

    # --- Usuarios ---
    @staticmethod
    def usuario_login() -> str:
        return "SELECT n_legajo, d_nombre FROM usuarios WHERE n_legajo = ? AND n_legajo = ?"

    @staticmethod
    def usuario_nombre() -> str:
        return "SELECT d_nombre FROM usuarios WHERE n_legajo = ?"
