"""
Módulo de base de datos
Maneja todas las conexiones y operaciones con la base de datos
"""

import pyodbc
import pandas as pd
import streamlit as st
from config import DATABASE_CONFIG, SQL_QUERIES


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
            if params:
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
        query = SQL_QUERIES["usuario_login"]
        result = self.execute_single_query(query, (legajo_int, password_int))

        if result:
            return True, result[1].strip() if result[1] else "Usuario"
        return False, None

    def obtener_nombre_usuario(self, legajo_int):
        """Obtiene el nombre de un usuario por su legajo"""
        query = SQL_QUERIES["usuario_nombre"]
        result = self.execute_single_query(query, (legajo_int,))

        if result:
            return result[0].strip() if result[0] else "Usuario"
        return None

    def consultar_recibos(self, comprobantes):
        """Consulta recibos por lista de comprobantes"""
        placeholders = ','.join(comprobantes)
        query = SQL_QUERIES["recibos"].format(placeholders=placeholders)
        return self.execute_query(query)

    def consultar_lotes_bancarios(self, conditions):
        """Consulta lotes bancarios con condiciones dinámicas"""
        where_clause = " AND ".join(conditions)
        query = SQL_QUERIES["lotes_bancarios"].format(where_clause=where_clause)
        return self.execute_query(query)

    def consultar_cuenta_corriente(self, all_conditions):
        """Consulta cuenta corriente con condiciones dinámicas"""
        where_clause = " AND ".join(all_conditions)
        query = SQL_QUERIES["cuenta_corriente"].format(where_clause=where_clause)
        return self.execute_query(query)

    def consultar_declaraciones_juradas(self, conditions):
        """Consulta declaraciones juradas con condiciones dinámicas"""
        where_clause = " AND ".join(conditions)
        query = SQL_QUERIES["declaraciones_juradas"].format(where_clause=where_clause)
        return self.execute_query(query)

    def consultar_declaraciones_juradas_adicional(self, conditions):
        """Consulta declaraciones juradas adicional con condiciones dinámicas"""
        where_clause = " AND ".join(conditions)
        query = SQL_QUERIES["declaraciones_juradas_adicional"].format(
            where_clause=where_clause
        )
        return self.execute_query(query)

    def consultar_planes(self, conditions):
        """Consulta los detalles del plan y sus cuotas"""
        where_clause = conditions
        query = SQL_QUERIES["planes"].format(where_clause=where_clause)
        return self.execute_query(query)

    def consultar_planes_cuotas(self, conditions):
        """Consulta las cuotas detalladas del plan"""
        where_clause = conditions
        query = SQL_QUERIES["planes_consulta_cuotas"].format(where_clause=where_clause)
        return self.execute_query(query)

    def consultar_planes_transacciones(self, conditions):
        """Consulta las transacciones asociadas al plan"""
        where_clause = conditions
        query = SQL_QUERIES["planes_transacciones"].format(where_clause=where_clause)
        return self.execute_query(query)


# Instancia global del manejador de base de datos
db_manager = DatabaseManager()
