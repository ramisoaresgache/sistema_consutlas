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
    def consultar_estadisticas_total_deuda(self, ano: int, cuota: int):
        """Obtiene el total de deuda para un año y cuota específicos."""
        query = SQLBuilder.estadisticas_total_deuda(ano, cuota)
        return self.execute_query(query)

    def consultar_estadisticas_por_localidad_directo(self, ano: int, cuota: int):
        """Obtiene los totales por localidad directamente sin tabla temporal."""
        query = SQLBuilder.estadisticas_emitido_por_zona_directo(ano, cuota)
        return self.execute_query(query)

    def consultar_estadisticas_pagos_sin_imputar_detalle(self, ano: int, cuota: int):
        """Obtiene el detalle de pagos que faltan por imputarse."""
        query = SQLBuilder.estadisticas_pagos_sin_imputar_detalle(ano, cuota)
        return self.execute_query(query)

    def consultar_estadisticas_pagos_sin_imputar_total(self, ano: int, cuota: int):
        """Obtiene el total de pagos que faltan por imputarse."""
        query = SQLBuilder.estadisticas_pagos_sin_imputar_total(ano, cuota)
        return self.execute_query(query)

    def consultar_estadisticas_pagos_confirmados_detalle(self, ano: int, cuota: int):
        """Obtiene el detalle de pagos confirmados."""
        query = SQLBuilder.estadisticas_pagos_confirmados_detalle(ano, cuota)
        return self.execute_query(query)

    def consultar_estadisticas_pagos_confirmados_total(self, ano: int, cuota: int):
        """Obtiene el total de pagos confirmados."""
        query = SQLBuilder.estadisticas_pagos_confirmados_total(ano, cuota)
        return self.execute_query(query)

    def consultar_estadisticas_pagos_deudores_detalle(self, ano: int, cuota: int):
        """Obtiene el detalle de pagos de deudores."""
        query = SQLBuilder.estadisticas_pagos_deudores_detalle(ano, cuota)
        return self.execute_query(query)

    def consultar_estadisticas_pagos_deudores_total(self, ano: int, cuota: int):
        """Obtiene el total de pagos de deudores."""
        query = SQLBuilder.estadisticas_pagos_deudores_total(ano, cuota)
        return self.execute_query(query)

    def crear_temp_emitido_por_zona(self, ano: int, cuota: int):
        """Crea la tabla temporal con emitido por zona."""
        conn = self.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = SQLBuilder.estadisticas_emitido_por_zona_temp(ano, cuota)
            cursor.execute(query)
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Error creando tabla temporal: {e}")
            return False
        finally:
            conn.close()

    def consultar_estadisticas_por_localidad(self):
        """Obtiene los totales por localidad desde la tabla temporal."""
        query = SQLBuilder.estadisticas_total_por_localidad()
        return self.execute_query(query)


# Instancia global del manejador de base de datos
db_manager = DatabaseManager()
