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
        if not columnas_metricas:
            return

        # Limitar a máximo 4 métricas para evitar error de índice en Streamlit
        metricas_items = list(columnas_metricas.items())[:4]
        num_metricas = len(metricas_items)

        if num_metricas == 0:
            return

        cols = st.columns(num_metricas)

        for i, (col_name, col_label) in enumerate(metricas_items):
            with cols[i]:
                try:
                    if col_name == "total":
                        st.metric(col_label, len(df))
                    elif col_name in df.columns:
                        # Verificar que la columna tenga datos válidos
                        if not df[col_name].isna().all():
                            unique_count = df[col_name].nunique()
                            st.metric(col_label, unique_count)
                        else:
                            st.metric(col_label, 0)
                    else:
                        # Si la columna no existe, mostrar 0
                        st.metric(col_label, 0)
                except Exception as e:
                    # En caso de error, mostrar métrica con valor 0
                    st.metric(col_label, 0)

    def _formatear_dataframe_por_tipos(self, df, filename_prefix):
        """Formatea las columnas del DataFrame de manera simple y robusta"""
        if df is None or df.empty:
            return df

        try:
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
                            df_display[col]
                            .astype(str)
                            .str.replace(",", "", regex=False)
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
                            df_display[col]
                            .astype(str)
                            .str.replace(",", "", regex=False)
                        )
                    except Exception:
                        # Si hay error, dejar la columna como está
                        pass

            return df_display
        except Exception as e:
            # Si hay cualquier error en el formateo, devolver el DataFrame original
            return df

    def mostrar_resultados(self, df, filename_prefix):
        """Muestra los resultados de una consulta con opción de descarga"""
        try:
            # Validar entrada
            if df is None:
                st.info("ℹ️ No se pudieron obtener resultados.")
                return

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

                st.success(
                    self.messages["search"]["results_found"].format(count=len(df))
                )

                # Formatear columnas según los tipos de datos correctos
                df_display = self._formatear_dataframe_por_tipos(df, filename_prefix)

                # Validar que df_display es válido antes de mostrarlo
                if df_display is not None and not df_display.empty:
                    # Mostrar dataframe con manejo de errores
                    try:
                        st.dataframe(df_display, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error al mostrar los datos: {str(e)}")
                        # Intentar mostrar el DataFrame original sin formatear
                        try:
                            st.dataframe(df, use_container_width=True)
                        except Exception as e2:
                            st.error(f"Error crítico al mostrar datos: {str(e2)}")
                            return

                    # Crear el botón de descarga con datos en session_state
                    self._crear_boton_descarga(df, filename_prefix)
                else:
                    st.error("Error: No se pudieron formatear los datos para mostrar.")
        except Exception as e:
            st.error(f"Error general en mostrar_resultados: {str(e)}")
            # Limpiar estado en caso de error
            session_key = f"last_results_{filename_prefix}"
            if session_key in st.session_state:
                del st.session_state[session_key]

    def _crear_boton_descarga(self, df, filename_prefix):
        """Crea el botón de descarga de Excel de manera robusta"""
        try:
            from io import BytesIO

            # Crear un contenedor para el botón
            download_container = st.container()

            with download_container:
                # Preparar los datos de Excel una sola vez
                excel_key = f"excel_data_{filename_prefix}"
                if excel_key not in st.session_state:
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Resultados")
                    st.session_state[excel_key] = output.getvalue()

                # Crear el botón usando los datos guardados
                if excel_key in st.session_state:
                    excel_data = st.session_state[excel_key]

                    st.download_button(
                        label=self.messages["search"]["download_button"],
                        data=excel_data,
                        file_name=f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_stable_{filename_prefix}",
                        help="Descargar resultados sin perder la búsqueda actual",
                    )
                else:
                    st.error("Error: No se pudieron preparar los datos para descarga.")
        except Exception as e:
            st.error(f"Error al crear botón de descarga: {str(e)}")

    def mostrar_resultados_persistentes(self, filename_prefix):
        """Muestra los resultados guardados en session_state si existen, solo datos sin botón de descarga"""
        try:
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

                # Validar que el DataFrame es válido
                if df is None or df.empty:
                    return False

                st.success(
                    self.messages["search"]["results_found"].format(count=len(df))
                )

                # Formatear columnas según los tipos de datos correctos
                df_display = self._formatear_dataframe_por_tipos(df, filename_prefix)

                # Validar que df_display es válido antes de mostrarlo
                if df_display is not None and not df_display.empty:
                    try:
                        # Mostrar solo el dataframe, SIN botón de descarga
                        st.dataframe(df_display, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error al mostrar datos persistentes: {str(e)}")
                        # Intentar mostrar el DataFrame original
                        try:
                            st.dataframe(df, use_container_width=True)
                        except Exception as e2:
                            st.error(
                                f"Error crítico al mostrar datos persistentes: {str(e2)}"
                            )
                            return False
                else:
                    st.error("Error: No se pudieron formatear los datos persistentes.")
                    return False

            return True
        except Exception as e:
            st.error(f"Error en mostrar_resultados_persistentes: {str(e)}")
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
        try:
            if spinner_container is not None:
                spinner_container.empty()
        except Exception:
            pass

        try:
            if cancel_container is not None:
                cancel_container.empty()
        except Exception:
            pass

        try:
            # Resetear flag de cancelación
            if cancel_key in st.session_state:
                st.session_state[cancel_key] = False
        except Exception:
            pass

    def validar_campos_requeridos(self, campos):
        """Valida que al menos un campo haya sido ingresado"""
        return any(campo.strip() for campo in campos)

    def mostrar_criterios_busqueda(
        self, criterios, titulo="🔍 Buscando con criterios", filename_prefix=None
    ):
        """Muestra los criterios de búsqueda"""
        try:
            if criterios:
                # Limpiar cualquier resultado persistente anterior
                if filename_prefix:
                    try:
                        result_container_key = (
                            f"persistent_results_container_{filename_prefix}"
                        )
                        if result_container_key in st.session_state:
                            st.session_state[result_container_key].empty()

                        # Para planes, también limpiar el contenedor de transacciones
                        if filename_prefix == "planes_consulta":
                            transacciones_container_key = "persistent_results_container_planes_transacciones_consulta"
                            if transacciones_container_key in st.session_state:
                                st.session_state[transacciones_container_key].empty()
                    except Exception:
                        pass

                # Limpiar criterios anteriores si existen
                try:
                    if "criterios_container" in st.session_state:
                        st.session_state["criterios_container"].empty()
                except Exception:
                    pass

                # Crear nuevo contenedor para criterios
                st.session_state["criterios_container"] = st.empty()

                # Mostrar los nuevos criterios
                try:
                    with st.session_state["criterios_container"].container():
                        st.info(f"{titulo}: {' | '.join(criterios)}")
                except Exception as e:
                    # Si hay error con el contenedor, mostrar directamente
                    st.info(f"{titulo}: {' | '.join(criterios)}")
        except Exception as e:
            # En caso de error total, mostrar mensaje básico
            st.info(f"🔍 Ejecutando búsqueda...")


# Instancia global de componentes UI
ui_components = UIComponents()
