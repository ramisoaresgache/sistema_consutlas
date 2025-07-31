"""
Sistema de Consultas - Archivo Principal
Aplicación modularizada para consultas de base de datos con autenticación
"""

import streamlit as st
from config import PAGE_CONFIG, TABS_CONFIG
from auth import auth_manager
from ui_components import ui_components
from consultas.recibos import consulta_recibos
from consultas.lotes_bancarios import consulta_lotes_bancarios
from consultas.cuenta_corriente import consulta_cuenta_corriente
from consultas.declaraciones_juradas import consulta_declaraciones_juradas
from consultas.planes import consulta_planes


def main():
    """Función principal de la aplicación"""

    # Configuración de la página
    st.set_page_config(**PAGE_CONFIG)

    # Inicializar sesión y verificar autenticación
    auth_manager.inicializar_sesion()

    # Si llegamos aquí, el usuario está logueado
    # Mostrar header con saludo y botón de logout
    ui_components.mostrar_header(auth_manager)

    st.markdown("---")

    # Crear pestañas principales reorganizadas
    tab_consultas, tab_reportes = st.tabs(["📊 Consultas", "📈 Reportes"])

    # PESTAÑA 1: CONSULTAS (contiene todas las consultas actuales)
    with tab_consultas:
        st.header("🔍 Módulos de Consulta")
        st.write("Seleccioná el tipo de consulta que querés realizar:")

        # Sub-pestañas para cada tipo de consulta
        subtab1, subtab2, subtab3, subtab4, subtab5 = st.tabs(
            [
                TABS_CONFIG["recibos"]["name"],
                TABS_CONFIG["lotes"]["name"],
                TABS_CONFIG["cuenta_corriente"]["name"],
                TABS_CONFIG["declaraciones_juradas"]["name"],
                TABS_CONFIG["planes"]["name"],
            ]
        )

        # SUB-PESTAÑA 1: CONSULTA DE RECIBOS
        with subtab1:
            consulta_recibos.mostrar_interfaz()

        # SUB-PESTAÑA 2: CONSULTA DE LOTES BANCARIOS
        with subtab2:
            consulta_lotes_bancarios.mostrar_interfaz()

        # SUB-PESTAÑA 3: CONSULTA DE CUENTA CORRIENTE
        with subtab3:
            consulta_cuenta_corriente.mostrar_interfaz()

        # SUB-PESTAÑA 4: CONSULTA DE DECLARACIONES JURADAS
        with subtab4:
            consulta_declaraciones_juradas.mostrar_interfaz()

        # SUB-PESTAÑA 5: CONSULTA DE PLANES
        with subtab5:
            consulta_planes.mostrar_interfaz()

    # PESTAÑA 2: REPORTES (nueva sección)
    with tab_reportes:
        st.header("📈 Módulos de Reportes")

        # Sub-pestañas para diferentes tipos de reportes
        subtab_clickup, subtab_estadisticos, subtab_dashboards = st.tabs(
            ["🎫 Tickets ClickUp", "📊 Reportes Estadísticos", "📈 Dashboards"]
        )

        # SUB-PESTAÑA 1: TICKETS CLICKUP
        with subtab_clickup:
            st.subheader("🎫 Gestión de Tickets ClickUp")
            st.write("Visualización y análisis de tickets del sistema ClickUp")

            # Botón para cargar datos
            if st.button("🔄 Cargar Datos de ClickUp", use_container_width=True):
                from reportes.clickup_manager import clickup_manager

                # Obtener datos
                df_clickup = clickup_manager.obtener_todas_las_tareas()

                if not df_clickup.empty:
                    # Guardar en session_state para persistencia
                    st.session_state.clickup_data = df_clickup
                    st.success(f"✅ Se cargaron {len(df_clickup)} tareas correctamente")
                else:
                    st.error("❌ No se pudieron cargar los datos de ClickUp")

            # Mostrar datos si existen en session_state
            if (
                "clickup_data" in st.session_state
                and not st.session_state.clickup_data.empty
            ):
                df = st.session_state.clickup_data

                # Mostrar métricas básicas
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("📊 Total Tareas", len(df))

                with col2:
                    espacios_unicos = df["Espacio"].nunique()
                    st.metric("🗂️ Espacios", espacios_unicos)

                with col3:
                    listas_unicas = df["Lista"].nunique()
                    st.metric("📋 Listas", listas_unicas)

                with col4:
                    asignados_unicos = (
                        df["Asignados"]
                        .apply(lambda x: len(x.split(", ")) if x else 0)
                        .sum()
                    )
                    st.metric("👥 Asignaciones", asignados_unicos)

                st.divider()

                # Filtros
                st.subheader("🔍 Filtros")

                # Agregar filtro de búsqueda por nombre como primera fila
                col_search = st.columns(1)[0]
                with col_search:
                    search_term = st.text_input(
                        "🔍 Buscar por nombre de tarea",
                        placeholder="Escribe parte del nombre de la tarea...",
                        help="Busca tareas que contengan el texto especificado en el nombre",
                    )

                # Filtros existentes en segunda fila
                col_filter1, col_filter2, col_filter3, col_filter4, col_filter5 = (
                    st.columns(5)
                )

                with col_filter1:
                    espacios = ["Todos"] + sorted(df["Espacio"].unique().tolist())
                    espacio_selected = st.selectbox("Espacio", espacios)

                with col_filter2:
                    estados = ["Todos"] + sorted(df["Estado"].unique().tolist())
                    estado_selected = st.selectbox("Estado", estados)

                with col_filter3:
                    prioridades = ["Todos"] + sorted(
                        [p for p in df["Prioridad"].unique() if p]
                    )
                    prioridad_selected = st.selectbox("Prioridad", prioridades)

                with col_filter4:
                    # Obtener fechas únicas sin duplicados y ordenar descendente
                    fechas_creacion_unicas = (
                        df["Fecha Creación"].dropna().dt.date.unique()
                    )
                    fechas_creacion = ["Todos"] + sorted(
                        [str(f) for f in fechas_creacion_unicas], reverse=True
                    )
                    fecha_selected = st.selectbox("Fecha Creación", fechas_creacion)

                with col_filter5:
                    # Obtener fechas únicas sin duplicados y ordenar descendente
                    fechas_cierre_unicas = df["Fecha Cierre"].dropna().dt.date.unique()
                    fechas_cierre = ["Todos"] + sorted(
                        [str(f) for f in fechas_cierre_unicas], reverse=True
                    )
                    fecha_cierre_selected = st.selectbox("Fecha Cierre", fechas_cierre)

                # Aplicar filtros
                df_filtered = df.copy()

                # Aplicar filtro de búsqueda por nombre (primero)
                if search_term:
                    # Mejorar el filtro de búsqueda
                    df_filtered = df_filtered[
                        df_filtered["Nombre"]
                        .astype(str)
                        .str.lower()
                        .str.contains(
                            search_term.lower().strip(),
                            case=False,
                            na=False,
                            regex=False,
                        )
                    ]

                if espacio_selected != "Todos":
                    df_filtered = df_filtered[
                        df_filtered["Espacio"] == espacio_selected
                    ]

                if estado_selected != "Todos":
                    df_filtered = df_filtered[df_filtered["Estado"] == estado_selected]

                if prioridad_selected != "Todos":
                    df_filtered = df_filtered[
                        df_filtered["Prioridad"] == prioridad_selected
                    ]

                if fecha_selected != "Todos":
                    # Filtrar por fecha de creación
                    df_filtered = df_filtered[
                        df_filtered["Fecha Creación"].dt.date.astype(str)
                        == fecha_selected
                    ]

                if fecha_cierre_selected != "Todos":
                    # Filtrar por fecha de cierre
                    df_filtered = df_filtered[
                        df_filtered["Fecha Cierre"].dt.date.astype(str)
                        == fecha_cierre_selected
                    ]

                st.divider()

                # Mostrar tabla filtrada
                st.subheader(f"✍🏼 Tareas ({len(df_filtered)} registros)")

                # Configurar columnas para mostrar
                columnas_mostrar = [
                    "ID",
                    "Nombre",
                    "Estado",
                    "Prioridad",
                    "Espacio",
                    "Lista",
                    "Asignados",
                    "Fecha Creación",
                    "Fecha Vencimiento",
                    "Fecha Cierre",
                    "Etiquetas",
                ]

                # Asegurar que las columnas existen
                columnas_disponibles = [
                    col for col in columnas_mostrar if col in df_filtered.columns
                ]

                if columnas_disponibles:
                    # Mostrar tabla con scroll horizontal
                    st.dataframe(
                        df_filtered[columnas_disponibles],
                        use_container_width=True,
                        height=400,
                    )

                    # Botón de descarga
                    if st.button("📥 Descargar datos filtrados como Excel"):
                        from io import BytesIO
                        import pandas as pd

                        buffer = BytesIO()
                        df_filtered.to_excel(buffer, index=False, engine="openpyxl")
                        buffer.seek(0)

                        st.download_button(
                            label="📥 Descargar Excel",
                            data=buffer.getvalue(),
                            file_name="tareas_clickup_filtradas.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )

                    # Agregar gráficos interactivos
                    st.divider()

                    # Importar y mostrar gráficos
                    try:
                        from reportes.clickup_charts import clickup_charts

                        clickup_charts.mostrar_todos_los_graficos(df_filtered)
                    except ImportError:
                        st.error(
                            "❌ No se pudo cargar el módulo de gráficos. Verificá que Plotly esté instalado."
                        )
                    except Exception as e:
                        st.error(f"❌ Error mostrando gráficos: {e}")

                else:
                    st.error("❌ No se encontraron columnas válidas para mostrar")
            else:
                st.info("ℹ️ Hacé clic en 'Cargar Datos de ClickUp' para comenzar")

        # SUB-PESTAÑA 2: REPORTES ESTADÍSTICOS
        with subtab_estadisticos:
            st.subheader("📊 Reportes Estadísticos")
            st.info("🚧 **Próximamente reportes estadísticos de recaudación**")

            st.markdown(
                """
            ### 📊 Reportes en Desarrollo
            
            En esta sección encontrarás:
            
            - 📈 **Reportes estadísticos** de recaudación
            - 📅 **Reportes programados** automáticos
            - 📋 **Análisis de tendencias** temporales
            - 💰 **Resúmenes ejecutivos** de gestión
            """
            )

        # SUB-PESTAÑA 3: DASHBOARDS
        with subtab_dashboards:
            st.subheader("📈 Dashboards Interactivos")
            st.info("🚧 **Próximamente dashboards interactivos**")

            st.markdown(
                """
            ### 📈 Dashboards en Desarrollo
            
            En esta sección encontrarás:
            
            - 📊 **Dashboards interactivos** con métricas
            - 📈 **Gráficos en tiempo real**
            - 🎯 **KPIs principales**
            - 📱 **Visualizaciones responsivas**
            """
            )

    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666; font-size: 0.8rem;">'
        "Sistema de la Municipalidad de Vicente López"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
