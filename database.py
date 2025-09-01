"""
Módulo de base de datos
Maneja todas las conexiones y operaciones con la base de datos
"""

import pyodbc
import pandas as pd
import streamlit as st
from config import DATABASE_CONFIG
from queries import SQLBuilder


class DatabaseManager:
    """Manejador de conexiones y consultas a la base de datos"""

    def __init__(self):
        self.conn_str = DATABASE_CONFIG["conn_str"]

    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        try:
            return pyodbc.connect(self.conn_str)
        except Exception as e:
            st.error(f"Error conectando a la base de datos: {e}")
            return None

    def execute_query(self, query, params=None):
        """Ejecuta una consulta y retorna un DataFrame"""
        conn = self.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            has_placeholders = "?" in str(query)
            if params and has_placeholders:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Obtener los nombres de las columnas
            columns = [desc[0] for desc in cursor.description]

            # Obtener todos los datos
            rows = cursor.fetchall()

            # Crear DataFrame manualmente
            df = pd.DataFrame([list(row) for row in rows], columns=columns)
            return df

        except Exception as e:
            st.error(f"Error ejecutando consulta: {e}")
            return None
        finally:
            conn.close()

    def execute_single_query(self, query, params=None):
        """Ejecuta una consulta que retorna un solo resultado"""
        conn = self.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Exception as e:
            st.error(f"Error ejecutando consulta: {e}")
            return None
        finally:
            conn.close()

    def verificar_usuario_login(self, legajo_int, password_int):
        """Verifica las credenciales de login del usuario"""
        query = SQLBuilder.usuario_login()
        result = self.execute_single_query(query, (legajo_int, password_int))
        if result:
            return True, result[1].strip() if result[1] else "Usuario"
        return False, None

    def obtener_nombre_usuario(self, legajo_int):
        """Obtiene el nombre de un usuario por su legajo"""
        query = SQLBuilder.usuario_nombre()
        result = self.execute_single_query(query, (legajo_int,))
        if result:
            return result[0].strip() if result[0] else "Usuario"
        return None

    def consultar_recibos(self, comprobantes):
        """Consulta recibos por lista de comprobantes"""
        placeholders = ','.join(comprobantes)
        query = SQLBuilder.recibos(placeholders)
        return self.execute_query(query)

    def consultar_lotes_bancarios(self, conditions):
        """Consulta lotes bancarios con condiciones dinámicas"""
        where_clause = " AND ".join(conditions)
        query = SQLBuilder.lotes_bancarios(where_clause)
        return self.execute_query(query)

    def consultar_cuenta_corriente(self, all_conditions):
        """Consulta cuenta corriente con condiciones dinámicas"""
        where_clause = " AND ".join(all_conditions)
        query = SQLBuilder.cuenta_corriente(where_clause)
        return self.execute_query(query)

    def consultar_declaraciones_juradas(self, conditions):
        """Consulta declaraciones juradas con condiciones dinámicas"""
        where_clause = " AND ".join(conditions)
        query = SQLBuilder.declaraciones_juradas(where_clause)
        return self.execute_query(query)

    def consultar_declaraciones_juradas_adicional(self, conditions):
        """Consulta declaraciones juradas adicional con condiciones dinámicas"""
        where_clause = " AND ".join(conditions)
        query = SQLBuilder.declaraciones_juradas_adicional(where_clause)
        return self.execute_query(query)

    def consultar_declaraciones_juradas_tercera(self, conditions):
        """Consulta declaraciones juradas tercera consulta con condiciones dinámicas"""
        where_clause = " AND ".join(conditions)
        query = SQLBuilder.declaraciones_juradas_detalle_simplificado(where_clause)
        return self.execute_query(query)

    def consultar_planes(self, conditions):
        """Consulta los detalles del plan y sus cuotas"""
        where_clause = conditions
        query = SQLBuilder.planes(where_clause)
        return self.execute_query(query)

    def consultar_planes_cuotas(self, conditions):
        """Consulta las cuotas detalladas del plan"""
        where_clause = conditions
        query = SQLBuilder.planes_consulta_cuotas(where_clause)
        return self.execute_query(query)

    def consultar_planes_transacciones(self, conditions):
        """Consulta las transacciones asociadas al plan"""
        where_clause = conditions
        query = SQLBuilder.planes_transacciones(where_clause)
        return self.execute_query(query)

    def consultar_debitos_abl(self, conditions):
        """Consulta los débitos automáticos de ABL"""
        where_clause = conditions
        query = SQLBuilder.debitos_abl(where_clause)
        return self.execute_query(query)

    def consultar_debitos_ppc_epagos(self, conditions):
        """Consulta los débitos automáticos de PPC ePagos"""
        where_clause = conditions
        query = SQLBuilder.debitos_ppc_epagos(where_clause)
        return self.execute_query(query)

    def consultar_cajas(self, comprobantes_list):
        """Consulta en la tabla cobros_cajas por número de comprobante."""
        if not comprobantes_list:
            return pd.DataFrame()
        
        # Asegurar que cada comprobante esté entre comillas simples para la consulta SQL
        comprobantes_quoted = [f"'{c}'" for c in comprobantes_list]
        comprobantes_str = ','.join(comprobantes_quoted)
        
        where_clause = f"n_comprob IN ({comprobantes_str})"
        query = SQLBuilder.consulta_cajas(where_clause)
        return self.execute_query(query)

    # --- NUEVAS: reportes estadísticos de recaudación ---
    def consultar_estadisticas_deuda_base(self, ano: int, cuota: int):
        """Devuelve filas de deuda base (n_orden=1, movimientos 207/249) sin CTE/param placeholders."""
        query = (
            "SELECT "
            "a.c_sistema, a.n_transac, a.c_cuenta, a.c_tasa, a.n_ano, a.n_cuota, a.c_actual, "
            "b.n_comprob, b.c_lugar_pago, b.i_capital, b.i_recargo, b.i_multa, b.c_movimiento, b.n_orden "
            "FROM transacciones a, cta_cte b "
            "WHERE a.n_transac = b.n_transac "
            f"AND a.n_ano = {int(ano)} "
            f"AND a.n_cuota = {int(cuota)} "
            "AND b.n_orden = 1 "
            "AND b.c_movimiento IN (207, 249)"
        )
        return self.execute_query(query)

    def consultar_estadisticas_pagos_realizados(self, ano: int, cuota: int):
        """Devuelve filas de pagos realizados (n_orden>1, movimiento=74) sin CTE/param placeholders."""
        query = (
            "SELECT "
            "a.c_sistema, a.n_transac, a.c_cuenta, a.c_tasa, a.n_ano, a.n_cuota, a.c_actual, "
            "b.n_comprob, b.c_lugar_pago, b.i_capital, b.i_recargo, b.i_multa, b.c_movimiento, b.n_orden "
            "FROM transacciones a, cta_cte b "
            "WHERE a.n_transac = b.n_transac "
            f"AND a.n_ano = {int(ano)} "
            f"AND a.n_cuota = {int(cuota)} "
            "AND b.n_orden > 1 "
            "AND b.c_movimiento = 74"
        )
        return self.execute_query(query)

    def consultar_estadisticas_pagos_pendientes(self, ano: int, cuota: int):
        """Devuelve DF vacío: 'pendientes' se calcula en Python como Deuda - Recaudado."""
        return pd.DataFrame()


# Instancia global del manejador de base de datos
db_manager = DatabaseManager()
