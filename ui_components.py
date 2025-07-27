"""
Componentes de interfaz de usuario
Elementos reutilizables de la UI
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from config import UI_CONFIG, MESSAGES


class UIComponents:
    """Componentes reutilizables de la interfaz de usuario"""

    def __init__(self):
        self.ui_config = UI_CONFIG
        self.messages = MESSAGES

    def mostrar_header(self, auth_manager):
        """Muestra el header principal con saludo y botón de logout"""
        col1, col2 = st.columns([10, 1])

        with col1:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; margin-top: -50px;">
                    <span style="font-size:3.2rem; font-weight: bold;">
                        {self.ui_config["header_title"]}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div style="text-align:left; margin-top: 30px;">
                    <span style="font-size:1.5rem;">
                        {self.ui_config["welcome_message"].format(nombre=st.session_state.user_nombre)}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                "<div style='text-align: right; margin-top: 30px; margin-right: 0px;'>",
                unsafe_allow_html=True,
            )
            if st.button(self.messages["session"]["logout_button"]):
                auth_manager.cerrar_sesion()
            st.markdown("</div>", unsafe_allow_html=True)

    def mostrar_estadisticas_basicas(self, df, columnas_metricas):
        """Muestra estadísticas básicas de los resultados"""
        cols = st.columns(len(columnas_metricas))

        for i, (col_name, col_label) in enumerate(columnas_metricas.items()):
            with cols[i]:
                if col_name == "total":
                    st.metric(col_label, len(df))
                elif col_name in df.columns:
                    st.metric(col_label, df[col_name].nunique())

    def mostrar_resultados(self, df, filename_prefix):
        """Muestra los resultados de una consulta con opción de descarga"""
        if df.empty:
            st.info(self.messages["search"]["no_results"])
        else:
            # Guardar resultados en session_state para persistir después de descarga
            session_key = f"last_results_{filename_prefix}"
            st.session_state[session_key] = df.copy()

            st.success(self.messages["search"]["results_found"].format(count=len(df)))

            # Formatear columnas específicas según el tipo de consulta
            df_display = df.copy()

            # Para recibos, formatear la columna comprobante sin comas
            if (
                filename_prefix == "recibos_consulta"
                and "comprobante" in df_display.columns
            ):
                df_display["comprobante"] = df_display["comprobante"].astype(str)

            # Para lotes bancarios, formatear la columna comprobante sin comas
            elif (
                filename_prefix in ["lotes_consulta", "bco_cab_consulta"]
                and "comprobante" in df_display.columns
            ):
                df_display["comprobante"] = df_display["comprobante"].astype(str)

            # Para cuenta corriente, formatear las columnas numéricas según su tipo
            elif filename_prefix in ["cuenta_corriente_consulta", "ctacte_consulta"]:
                # Identificadores enteros (sin comas)
                if "comprobante" in df_display.columns:
                    df_display["comprobante"] = (
                        df_display["comprobante"].astype(str).str.replace(",", "")
                    )
                if "transaccion" in df_display.columns:
                    df_display["transaccion"] = (
                        df_display["transaccion"].astype(str).str.replace(",", "")
                    )
                if "cuenta" in df_display.columns:
                    df_display["cuenta"] = (
                        df_display["cuenta"].astype(str).str.replace(",", "")
                    )

                # Campos smallint (sin comas)
                if "ano" in df_display.columns:
                    df_display["ano"] = (
                        df_display["ano"].astype(str).str.replace(",", "")
                    )
                if "cuota" in df_display.columns:
                    df_display["cuota"] = (
                        df_display["cuota"].astype(str).str.replace(",", "")
                    )
                if "tasa" in df_display.columns:
                    df_display["tasa"] = (
                        df_display["tasa"].astype(str).str.replace(",", "")
                    )

                # Campos decimales (mantener formato decimal pero sin comas de miles)
                for col in ["importe", "recargo", "multa"]:
                    if col in df_display.columns:
                        # Limpiar formato y convertir a string sin comas
                        df_display[col] = (
                            df_display[col].astype(str).str.replace(",", "")
                        )

            # Para declaraciones juradas, formatear las columnas numéricas que son identificadores
            elif filename_prefix in [
                "declaraciones_juradas_consulta",
                "declaraciones_juradas_adicional",
            ]:
                if "cuit" in df_display.columns:
                    df_display["cuit"] = (
                        df_display["cuit"].astype(str).str.replace(",", "")
                    )
                if "cuenta" in df_display.columns:
                    df_display["cuenta"] = (
                        df_display["cuenta"].astype(str).str.replace(",", "")
                    )
                if "id_simplificado" in df_display.columns:
                    df_display["id_simplificado"] = (
                        df_display["id_simplificado"].astype(str).str.replace(",", "")
                    )

            # Para planes, formatear las columnas numéricas según su tipo
            elif filename_prefix in [
                "planes_consulta",
                "planes_transacciones_consulta",
            ]:
                # Identificadores enteros (sin comas)
                if "plan" in df_display.columns:
                    df_display["plan"] = (
                        df_display["plan"].astype(str).str.replace(",", "")
                    )
                if "cuota_plan" in df_display.columns:
                    df_display["cuota_plan"] = (
                        df_display["cuota_plan"].astype(str).str.replace(",", "")
                    )
                if "cantidad_cuotas" in df_display.columns:
                    df_display["cantidad_cuotas"] = (
                        df_display["cantidad_cuotas"].astype(str).str.replace(",", "")
                    )
                if "porcentaje_anticipo" in df_display.columns:
                    df_display["porcentaje_anticipo"] = (
                        df_display["porcentaje_anticipo"]
                        .astype(str)
                        .str.replace(",", "")
                    )

                # Campos similares a cuenta corriente
                if "comprobante" in df_display.columns:
                    df_display["comprobante"] = (
                        df_display["comprobante"].astype(str).str.replace(",", "")
                    )
                if "transaccion" in df_display.columns:
                    df_display["transaccion"] = (
                        df_display["transaccion"].astype(str).str.replace(",", "")
                    )
                if "cuenta" in df_display.columns:
                    df_display["cuenta"] = (
                        df_display["cuenta"].astype(str).str.replace(",", "")
                    )
                if "ano" in df_display.columns:
                    df_display["ano"] = (
                        df_display["ano"].astype(str).str.replace(",", "")
                    )
                if "cuota" in df_display.columns:
                    df_display["cuota"] = (
                        df_display["cuota"].astype(str).str.replace(",", "")
                    )
                if "tasa" in df_display.columns:
                    df_display["tasa"] = (
                        df_display["tasa"].astype(str).str.replace(",", "")
                    )
                if "orden" in df_display.columns:
                    df_display["orden"] = (
                        df_display["orden"].astype(str).str.replace(",", "")
                    )

                # Campos decimales (sin comas de miles)
                for col in [
                    "importe_anticipo",
                    "capital_cuota",
                    "recargos_cuotas",
                    "intereses_cuota",
                    "multa",
                    "importe",
                    "recargo",
                ]:
                    if col in df_display.columns:
                        df_display[col] = (
                            df_display[col].astype(str).str.replace(",", "")
                        )

            # Mostrar dataframe
            st.dataframe(df_display, use_container_width=True)

            # Crear el botón de descarga con datos en session_state
            self._crear_boton_descarga(df, filename_prefix)

    def _crear_boton_descarga(self, df, filename_prefix):
        """Crea el botón de descarga de Excel de manera robusta"""
        from io import BytesIO

        # Crear un contenedor para el botón
        download_container = st.container()

        with download_container:
            # Preparar los datos de Excel una sola vez
            if f"excel_data_{filename_prefix}" not in st.session_state:
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Resultados")
                st.session_state[f"excel_data_{filename_prefix}"] = output.getvalue()

            # Crear el botón usando los datos guardados
            excel_data = st.session_state[f"excel_data_{filename_prefix}"]

            st.download_button(
                label=self.messages["search"]["download_button"],
                data=excel_data,
                file_name=f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"download_stable_{filename_prefix}",
                help="Descargar resultados sin perder la búsqueda actual",
            )

    def mostrar_resultados_persistentes(self, filename_prefix):
        """Muestra los resultados guardados en session_state si existen"""
        session_key = f"last_results_{filename_prefix}"
        if session_key in st.session_state:
            st.info("📋 Mostrando resultados de la última búsqueda:")
            self.mostrar_resultados(st.session_state[session_key], filename_prefix)
            return True
        return False

    def crear_controles_busqueda(self, key_prefix):
        """Crea controles para cancelar búsqueda"""
        # Crear contenedores para el spinner y botón de cancelar
        spinner_container = st.empty()
        cancel_container = st.empty()

        # Variable para controlar la cancelación
        cancel_key = f"cancel_search_{key_prefix}"
        if cancel_key not in st.session_state:
            st.session_state[cancel_key] = False

        return spinner_container, cancel_container, cancel_key

    def mostrar_boton_cancelar(self, cancel_container, key_prefix):
        """Muestra el botón de cancelar búsqueda"""
        with cancel_container.container():
            if st.button(
                self.messages["search"]["cancel_button"],
                key=f"cancel_{key_prefix}",
                use_container_width=True,
            ):
                st.session_state[f"cancel_search_{key_prefix}"] = True
                st.warning(self.messages["search"]["cancelled"])
                st.stop()

    def ejecutar_con_spinner(self, spinner_container, mensaje, funcion_consulta):
        """Ejecuta una función con spinner de progreso"""
        with spinner_container.container():
            with st.spinner(mensaje):
                return funcion_consulta()

    def limpiar_controles(self, spinner_container, cancel_container, cancel_key):
        """Limpia los controles de búsqueda"""
        spinner_container.empty()
        cancel_container.empty()
        # Resetear flag de cancelación
        st.session_state[cancel_key] = False

    def validar_campos_requeridos(self, campos):
        """Valida que al menos un campo haya sido ingresado"""
        return any(campo.strip() for campo in campos)

    def mostrar_criterios_busqueda(self, criterios, titulo="🔍 Buscando con criterios"):
        """Muestra los criterios de búsqueda"""
        if criterios:
            st.info(f"{titulo}: {' | '.join(criterios)}")


# Instancia global de componentes UI
ui_components = UIComponents()
