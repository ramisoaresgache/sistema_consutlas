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

    def _formatear_dataframe_por_tipos(self, df, filename_prefix):
        """Formatea las columnas del DataFrame de manera simple y robusta"""
        df_display = df.copy()

        # Lista de campos que sabemos que son identificadores numéricos (sin comas)
        campos_numericos_sin_comas = [
            "sistema",
            "comprobante",
            "cuenta",
            "tasa",
            "ano",
            "cuota",
            "transaccion",
            "orden",
            "numero_lote",
            "numero_plan",
            "cuit",
            "id_simplificado",
            "rubro_principal",
            "plan",
            "cantidad_cuotas",
            "cuota_plan",
        ]

        # Formatear solo los campos que existen en el DataFrame
        for col in campos_numericos_sin_comas:
            if col in df_display.columns:
                try:
                    # Convertir a string y remover comas si existen
                    df_display[col] = (
                        df_display[col].astype(str).str.replace(",", "", regex=False)
                    )
                except Exception:
                    # Si hay error, dejar la columna como está
                    pass

        # Para campos decimales (importes), también remover comas pero mantener puntos decimales
        campos_decimales = [
            "importe",
            "recargo",
            "multa",
            "recargos",
            "importe_anticipo",
            "capital_cuota",
            "recargos_cuotas",
            "intereses_cuota",
            "porcentaje_anticipo",
        ]

        for col in campos_decimales:
            if col in df_display.columns:
                try:
                    # Convertir a string y remover solo comas (mantener puntos decimales)
                    df_display[col] = (
                        df_display[col].astype(str).str.replace(",", "", regex=False)
                    )
                except Exception:
                    # Si hay error, dejar la columna como está
                    pass

        return df_display

    def mostrar_resultados(self, df, filename_prefix):
        """Muestra los resultados de una consulta con opción de descarga"""
        # Limpiar cualquier contenedor de criterios de búsqueda anterior
        if "criterios_container" in st.session_state:
            st.session_state["criterios_container"].empty()
            del st.session_state["criterios_container"]

        # Limpiar contenedor de resultados persistentes para evitar duplicados
        result_container_key = f"persistent_results_container_{filename_prefix}"
        if result_container_key in st.session_state:
            st.session_state[result_container_key].empty()
            del st.session_state[result_container_key]

        # Limpiar datos de Excel anteriores para forzar la regeneración
        excel_key = f"excel_data_{filename_prefix}"
        if excel_key in st.session_state:
            del st.session_state[excel_key]

        if df.empty:
            st.info(self.messages["search"]["no_results"])
            # Si no hay resultados, asegurarse de que no queden resultados persistentes
            session_key = f"last_results_{filename_prefix}"
            if session_key in st.session_state:
                del st.session_state[session_key]
        else:
            # Guardar resultados en session_state para persistir después de descarga
            session_key = f"last_results_{filename_prefix}"
            st.session_state[session_key] = df.copy()

            st.success(self.messages["search"]["results_found"].format(count=len(df)))

            # Formatear columnas según los tipos de datos correctos
            df_display = self._formatear_dataframe_por_tipos(df, filename_prefix)

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
        """Muestra los resultados guardados en session_state si existen, solo datos sin botón de descarga"""
        session_key = f"last_results_{filename_prefix}"

        # Verificar si hay resultados válidos para mostrar
        if (
            session_key not in st.session_state
            or st.session_state[session_key] is None
            or st.session_state[session_key].empty
        ):
            return False

        # Crear un contenedor específico para los resultados persistentes
        result_container_key = f"persistent_results_container_{filename_prefix}"
        if result_container_key not in st.session_state:
            st.session_state[result_container_key] = st.empty()

        with st.session_state[result_container_key].container():
            st.info("📋 Mostrando resultados de la última búsqueda:")
            df = st.session_state[session_key]

            st.success(self.messages["search"]["results_found"].format(count=len(df)))

            # Formatear columnas según los tipos de datos correctos
            df_display = self._formatear_dataframe_por_tipos(df, filename_prefix)

            # Mostrar solo el dataframe, SIN botón de descarga
            st.dataframe(df_display, use_container_width=True)

        return True

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

    def mostrar_criterios_busqueda(
        self, criterios, titulo="🔍 Buscando con criterios", filename_prefix=None
    ):
        """Muestra los criterios de búsqueda"""
        if criterios:
            # Limpiar cualquier resultado persistente anterior
            if filename_prefix:
                result_container_key = f"persistent_results_container_{filename_prefix}"
                if result_container_key in st.session_state:
                    st.session_state[result_container_key].empty()

                # Para planes, también limpiar el contenedor de transacciones
                if filename_prefix == "planes_consulta":
                    transacciones_container_key = (
                        "persistent_results_container_planes_transacciones_consulta"
                    )
                    if transacciones_container_key in st.session_state:
                        st.session_state[transacciones_container_key].empty()

            # Limpiar criterios anteriores si existen
            if "criterios_container" in st.session_state:
                st.session_state["criterios_container"].empty()

            # Crear nuevo contenedor para criterios
            st.session_state["criterios_container"] = st.empty()

            # Mostrar los nuevos criterios
            with st.session_state["criterios_container"].container():
                st.info(f"{titulo}: {' | '.join(criterios)}")


# Instancia global de componentes UI
ui_components = UIComponents()
