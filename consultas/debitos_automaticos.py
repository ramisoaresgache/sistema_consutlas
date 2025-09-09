"""
Módulo de consulta de débitos automáticos
Maneja las consultas de débitos de ABL y PPC ePagos
"""

import streamlit as st
import pandas as pd
from database import db_manager
from config import MESSAGES


class ConsultaDebitosAutomaticos:
    """Manejador de consultas de débitos automáticos"""

    def _validar_campos_abl(self, cuentas):
        """Valida los campos de entrada para débitos ABL"""
        if not cuentas:
            st.error("⚠️ Ingresá al menos una cuenta para buscar.")
            return False
        return True

    def _validar_campos_ppc(self, planes, cuit):
        """Valida los campos de entrada para débitos PPC ePagos"""
        if not planes and not cuit:
            st.error("⚠️ Ingresá al menos un plan o un CUIT para buscar.")
            return False
        return True

    def _preparar_where_clause_abl(self, cuentas):
        """Prepara la cláusula WHERE para débitos ABL"""
        cuentas_list = [cuenta.strip() for cuenta in cuentas.split(",") if cuenta.strip()]
        
        if len(cuentas_list) == 1:
            return f"a.c_cuenta = '{cuentas_list[0]}'"
        else:
            cuentas_str = "', '".join(cuentas_list)
            return f"a.c_cuenta IN ('{cuentas_str}')"

    def _preparar_where_clause_ppc(self, planes, cuit):
        """Prepara la cláusula WHERE para débitos PPC ePagos"""
        if planes and cuit:
            # Si se proporcionan ambos, buscar por planes O por CUIT
            planes_list = [plan.strip() for plan in planes.split(",") if plan.strip()]
            if len(planes_list) == 1:
                return f"IN ({planes_list[0]}, (SELECT n_plan FROM ppc_epagos_debito_directo_registrados WHERE n_cuit = '{cuit.strip()}'))"
            else:
                planes_str = ", ".join(planes_list)
                return f"IN ({planes_str}, (SELECT n_plan FROM ppc_epagos_debito_directo_registrados WHERE n_cuit = '{cuit.strip()}'))"
        elif planes:
            # Solo planes
            planes_list = [plan.strip() for plan in planes.split(",") if plan.strip()]
            if len(planes_list) == 1:
                return f"= {planes_list[0]}"
            else:
                planes_str = ", ".join(planes_list)
                return f"IN ({planes_str})"
        elif cuit:
            # Solo CUIT
            return f"IN (SELECT n_plan FROM ppc_epagos_debito_directo_registrados WHERE n_cuit = '{cuit.strip()}')"
        else:
            return "= 0"  # No debería llegar aquí debido a validación

    def consultar_debitos_abl(self, cuentas):
        """Realiza la consulta de débitos ABL"""
        try:
            where_clause = self._preparar_where_clause_abl(cuentas)
            resultado = db_manager.consultar_debitos_abl(where_clause)
            return resultado
            
        except Exception as e:
            st.error(f"Error al consultar débitos ABL: {str(e)}")
            return pd.DataFrame()

    def consultar_debitos_ppc(self, planes, cuit):
        """Realiza la consulta de débitos PPC ePagos"""
        try:
            where_clause = self._preparar_where_clause_ppc(planes, cuit)
            resultado = db_manager.consultar_debitos_ppc_epagos(where_clause)
            return resultado
            
        except Exception as e:
            st.error(f"Error al consultar débitos PPC ePagos: {str(e)}")
            return pd.DataFrame()

    def mostrar_interfaz(self):
        """Muestra la interfaz de consulta de débitos automáticos"""
        st.header("🏦 Consulta de Débitos Automáticos")
        st.write("Consultá débitos automáticos de ABL y PPC ePagos.")

        # Crear pestañas para los dos tipos de débitos
        tab_abl, tab_ppc = st.tabs(["💳 Débitos ABL", "💰 Débitos PPC ePagos"])

        # PESTAÑA 1: DÉBITOS ABL
        with tab_abl:
            st.subheader("💳 Consulta de Débitos ABL")
            st.write("Consultá los débitos automáticos de ABL por cuenta.")

            # Formulario de búsqueda ABL
            with st.form("form_debitos_abl"):
                cuentas_abl = st.text_input(
                    "Cuenta/s ABL:",
                    placeholder="Ej: 123456 o 123456, 789012 (separadas por comas)",
                    help="Ingresá una o más cuentas separadas por comas"
                )
                
                submitted_abl = st.form_submit_button("🔍 Buscar Débitos ABL")

            # Procesar búsqueda ABL
            if submitted_abl:
                if self._validar_campos_abl(cuentas_abl):
                    with st.spinner("Buscando débitos ABL..."):
                        df_resultado = self.consultar_debitos_abl(cuentas_abl)
                        
                        if not df_resultado.empty:
                            st.success(f"✅ Se encontraron {len(df_resultado)} registros de débitos ABL:")
                            st.dataframe(df_resultado, use_container_width=True)
                            
                            # Botón de descarga directo
                            from io import BytesIO
                            buffer = BytesIO()
                            df_resultado.to_excel(buffer, index=False, engine="openpyxl")
                            buffer.seek(0)
                            
                            st.download_button(
                                label="📥 Descargar como Excel",
                                data=buffer.getvalue(),
                                file_name="debitos_abl.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="download_abl_excel"
                            )
                        else:
                            st.info("ℹ️ No se encontraron débitos ABL para las cuentas especificadas.")

        # PESTAÑA 2: DÉBITOS PPC EPAGOS
        with tab_ppc:
            st.subheader("💰 Consulta de Débitos PPC ePagos")
            st.write("Consultá los débitos automáticos de PPC ePagos por plan o CUIT.")

            # Formulario de búsqueda PPC
            with st.form("form_debitos_ppc"):
                col1, col2 = st.columns(2)
                
                with col1:
                    planes_ppc = st.text_input(
                        "Plan/es de Pago:",
                        placeholder="Ej: 12345 o 12345, 67890 (separados por comas)",
                        help="Ingresá uno o más planes separados por comas"
                    )
                
                with col2:
                    cuit_ppc = st.text_input(
                        "CUIT:",
                        placeholder="Ej: 20123456789",
                        help="Ingresá un CUIT para buscar sus planes"
                    )
                
                st.info("💡 Podés buscar por plan/es, por CUIT, o por ambos.")
                
                submitted_ppc = st.form_submit_button("🔍 Buscar Débitos PPC ePagos")

            # Procesar búsqueda PPC
            if submitted_ppc:
                if self._validar_campos_ppc(planes_ppc, cuit_ppc):
                    with st.spinner("Buscando débitos PPC ePagos..."):
                        df_resultado = self.consultar_debitos_ppc(planes_ppc, cuit_ppc)
                        
                        if not df_resultado.empty:
                            st.success(f"✅ Se encontraron {len(df_resultado)} registros de débitos PPC ePagos:")
                            st.dataframe(df_resultado, use_container_width=True)
                            
                            # Botón de descarga directo
                            from io import BytesIO
                            buffer = BytesIO()
                            df_resultado.to_excel(buffer, index=False, engine="openpyxl")
                            buffer.seek(0)
                            
                            st.download_button(
                                label="📥 Descargar como Excel",
                                data=buffer.getvalue(),
                                file_name="debitos_ppc_epagos.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="download_ppc_excel"
                            )
                        else:
                            st.info("ℹ️ No se encontraron débitos PPC ePagos para los criterios especificados.")


# Instancia global del manejador
consulta_debitos_automaticos = ConsultaDebitosAutomaticos()
