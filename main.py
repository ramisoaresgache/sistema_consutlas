"""
Sistema de Consultas - Archivo Principal
Aplicación modularizada para consultas de base de datos con autenticación
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config import PAGE_CONFIG, TABS_CONFIG
from auth import auth_manager
from ui_components import ui_components
from consultas.recibos import consulta_recibos
from consultas.lotes_bancarios import consulta_lotes_bancarios
from consultas.cuenta_corriente import consulta_cuenta_corriente
from consultas.declaraciones_juradas import consulta_declaraciones_juradas
from consultas.planes import consulta_planes
from consultas.debitos_automaticos import consulta_debitos_automaticos


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
        subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs(
            [
                TABS_CONFIG["recibos"]["name"],
                TABS_CONFIG["lotes"]["name"],
                TABS_CONFIG["cuenta_corriente"]["name"],
                TABS_CONFIG["declaraciones_juradas"]["name"],
                TABS_CONFIG["planes"]["name"],
                TABS_CONFIG["debitos_automaticos"]["name"],
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

        # SUB-PESTAÑA 6: CONSULTA DE DÉBITOS AUTOMÁTICOS
        with subtab6:
            consulta_debitos_automaticos.mostrar_interfaz()

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
                    st.metric("🗂️ Espacios ", espacios_unicos)

                # with col3:
                #     listas_unicas = df["Lista"].nunique()
                #     st.metric("📋 Listas", listas_unicas)

                with col3:
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
                col_filter1, col_filter2, col_filter3, col_filter4, col_filter5, col_filter6 = (
                    st.columns(6)
                )

                with col_filter1:
                    espacios_disponibles = sorted(df["Espacio"].unique().tolist())
                    espacios_selected = st.multiselect(
                        "Espacios (múltiple)", 
                        espacios_disponibles,
                        help="Selecciona uno o múltiples espacios. Si no seleccionas ninguno, se mostrarán todos."
                    )

                with col_filter2:
                    estados_disponibles = sorted(df["Estado"].unique().tolist())
                    estados_selected = st.multiselect(
                        "Estados (múltiple)", 
                        estados_disponibles,
                        help="Selecciona uno o múltiples estados. Si no seleccionas ninguno, se mostrarán todos."
                    )

                with col_filter3:
                    all_tags = set()
                    # La columna 'Etiquetas' puede contener strings de tags separados por comas
                    df['Etiquetas'].dropna().apply(
                        lambda x: all_tags.update([tag.strip() for tag in str(x).split(',') if tag.strip()])
                    )
                    etiquetas_disponibles = sorted(list(all_tags))
                    etiquetas_selected = st.multiselect(
                        "Etiquetas (múltiple)",
                        etiquetas_disponibles,
                        help="Selecciona una o múltiples etiquetas para filtrar las tareas."
                    )

                with col_filter4:
                    st.write("**Rango Fecha Creación**")
                    
                    # Checkbox para activar/desactivar filtro
                    usar_filtro_creacion = st.checkbox(
                        "Filtrar por fecha de creación",
                        value=False,
                        key="checkbox_fecha_creacion"
                    )
                    
                    if usar_filtro_creacion:
                        # Obtener rango de fechas de creación
                        fechas_creacion_min = df["Fecha Creación"].dropna().dt.date.min()
                        fechas_creacion_max = df["Fecha Creación"].dropna().dt.date.max()
                        
                        if fechas_creacion_min and fechas_creacion_max:
                            # Usar un rango más amplio para permitir flexibilidad
                            from datetime import date
                            min_date_allowed = date(2020, 1, 1)  # Fecha mínima permitida
                            max_date_allowed = date(2030, 12, 31)  # Fecha máxima permitida
                            
                            fecha_creacion_desde = st.date_input(
                                "Desde:", 
                                value=fechas_creacion_min,
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_creacion_desde"
                            )
                            fecha_creacion_hasta = st.date_input(
                                "Hasta:", 
                                value=fechas_creacion_max,
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_creacion_hasta"
                            )
                        else:
                            fecha_creacion_desde = None
                            fecha_creacion_hasta = None
                    else:
                        fecha_creacion_desde = None
                        fecha_creacion_hasta = None

                with col_filter5:
                    st.write("**Rango Fecha Cierre**")
                    
                    # Checkbox para activar/desactivar filtro
                    usar_filtro_cierre = st.checkbox(
                        "Filtrar por fecha de cierre",
                        value=False,
                        key="checkbox_fecha_cierre"
                    )
                    
                    if usar_filtro_cierre:
                        # Obtener rango de fechas de cierre
                        fechas_cierre_validas = df["Fecha Cierre"].dropna()
                        
                        if not fechas_cierre_validas.empty:
                            fechas_cierre_min = fechas_cierre_validas.dt.date.min()
                            fechas_cierre_max = fechas_cierre_validas.dt.date.max()
                            
                            # Usar un rango más amplio para permitir flexibilidad
                            from datetime import date
                            min_date_allowed = date(2020, 1, 1)  # Fecha mínima permitida
                            max_date_allowed = date(2030, 12, 31)  # Fecha máxima permitida
                            
                            fecha_cierre_desde = st.date_input(
                                "Desde:", 
                                value=fechas_cierre_min,
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_cierre_desde"
                            )
                            fecha_cierre_hasta = st.date_input(
                                "Hasta:", 
                                value=fechas_cierre_max,
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_cierre_hasta"
                            )
                        else:
                            # Si no hay fechas de cierre, usar valores por defecto
                            from datetime import date
                            min_date_allowed = date(2020, 1, 1)
                            max_date_allowed = date(2030, 12, 31)
                            
                            fecha_cierre_desde = st.date_input(
                                "Desde:", 
                                value=date.today(),
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_cierre_desde"
                            )
                            fecha_cierre_hasta = st.date_input(
                                "Hasta:", 
                                value=date.today(),
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_cierre_hasta"
                            )
                            st.info("ℹ️ No hay tareas con fecha de cierre en los datos. Puedes seleccionar cualquier rango.")
                    else:
                        fecha_cierre_desde = None
                        fecha_cierre_hasta = None

                with col_filter6:
                    st.write("**Rango Fecha Vencimiento**")
                    
                    # Checkbox para activar/desactivar filtro
                    usar_filtro_vencimiento = st.checkbox(
                        "Filtrar por fecha de vencimiento",
                        value=False,
                        key="checkbox_fecha_vencimiento"
                    )
                    
                    if usar_filtro_vencimiento:
                        # Obtener rango de fechas de vencimiento
                        fechas_vencimiento_validas = df["Fecha Vencimiento"].dropna()
                        
                        if not fechas_vencimiento_validas.empty:
                            fechas_vencimiento_min = fechas_vencimiento_validas.dt.date.min()
                            fechas_vencimiento_max = fechas_vencimiento_validas.dt.date.max()
                            
                            # Usar un rango más amplio para permitir flexibilidad
                            from datetime import date
                            min_date_allowed = date(2020, 1, 1)  # Fecha mínima permitida
                            max_date_allowed = date(2030, 12, 31)  # Fecha máxima permitida
                            
                            fecha_vencimiento_desde = st.date_input(
                                "Desde:", 
                                value=fechas_vencimiento_min,
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_vencimiento_desde"
                            )
                            fecha_vencimiento_hasta = st.date_input(
                                "Hasta:", 
                                value=fechas_vencimiento_max,
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_vencimiento_hasta"
                            )
                        else:
                            # Si no hay fechas de vencimiento, usar valores por defecto
                            from datetime import date
                            min_date_allowed = date(2020, 1, 1)
                            max_date_allowed = date(2030, 12, 31)
                            
                            fecha_vencimiento_desde = st.date_input(
                                "Desde:", 
                                value=date.today(),
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_vencimiento_desde"
                            )
                            fecha_vencimiento_hasta = st.date_input(
                                "Hasta:", 
                                value=date.today(),
                                min_value=min_date_allowed,
                                max_value=max_date_allowed,
                                key="fecha_vencimiento_hasta"
                            )
                            st.info("ℹ️ No hay tareas con fecha de vencimiento en los datos. Puedes seleccionar cualquier rango.")
                    else:
                        fecha_vencimiento_desde = None
                        fecha_vencimiento_hasta = None

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

                # Aplicar filtro de espacios (selección múltiple)
                if espacios_selected:  # Si hay espacios seleccionados
                    df_filtered = df_filtered[
                        df_filtered["Espacio"].isin(espacios_selected)
                    ]

                # Aplicar filtro de estados (selección múltiple)
                if estados_selected:  # Si hay estados seleccionados
                    df_filtered = df_filtered[df_filtered["Estado"].isin(estados_selected)]

                # Aplicar filtro de etiquetas (selección múltiple)
                if etiquetas_selected:
                    # Filtrar tareas que contengan CUALQUIERA de las etiquetas seleccionadas
                    df_filtered = df_filtered[
                        df_filtered['Etiquetas'].dropna().apply(
                            lambda x: any(tag.strip() in etiquetas_selected for tag in str(x).split(','))
                        )
                    ]

                # Aplicar filtro de rango de fecha de creación
                if fecha_creacion_desde and fecha_creacion_hasta:
                    # Asegurar que la fecha "desde" no sea mayor que "hasta"
                    if fecha_creacion_desde <= fecha_creacion_hasta:
                        # Convertir las fechas a datetime para comparación segura
                        fecha_desde_dt = datetime.combine(fecha_creacion_desde, datetime.min.time())
                        fecha_hasta_dt = datetime.combine(fecha_creacion_hasta, datetime.max.time())
                        
                        # Filtrar solo registros con fechas válidas (no NaT)
                        mask_fecha_creacion = (
                            df_filtered["Fecha Creación"].notna() &
                            (df_filtered["Fecha Creación"] >= fecha_desde_dt) &
                            (df_filtered["Fecha Creación"] <= fecha_hasta_dt)
                        )
                        df_filtered = df_filtered[mask_fecha_creacion]
                    else:
                        st.warning("⚠️ La fecha 'desde' de creación no puede ser mayor que la fecha 'hasta'")

                # Aplicar filtro de rango de fecha de cierre
                if fecha_cierre_desde and fecha_cierre_hasta:
                    # Asegurar que la fecha "desde" no sea mayor que "hasta"
                    if fecha_cierre_desde <= fecha_cierre_hasta:
                        # Convertir las fechas a datetime para comparación segura
                        fecha_desde_dt = datetime.combine(fecha_cierre_desde, datetime.min.time())
                        fecha_hasta_dt = datetime.combine(fecha_cierre_hasta, datetime.max.time())
                        
                        # Filtrar solo registros con fechas válidas (no NaT)
                        mask_fecha_cierre = (
                            df_filtered["Fecha Cierre"].notna() &
                            (df_filtered["Fecha Cierre"] >= fecha_desde_dt) &
                            (df_filtered["Fecha Cierre"] <= fecha_hasta_dt)
                        )
                        df_filtered = df_filtered[mask_fecha_cierre]
                    else:
                        st.warning("⚠️ La fecha 'desde' de cierre no puede ser mayor que la fecha 'hasta'")

                # Aplicar filtro de rango de fecha de vencimiento
                if fecha_vencimiento_desde and fecha_vencimiento_hasta:
                    # Asegurar que la fecha "desde" no sea mayor que "hasta"
                    if fecha_vencimiento_desde <= fecha_vencimiento_hasta:
                        # Convertir las fechas a datetime para comparación segura
                        fecha_desde_dt = datetime.combine(fecha_vencimiento_desde, datetime.min.time())
                        fecha_hasta_dt = datetime.combine(fecha_vencimiento_hasta, datetime.max.time())
                        
                        # Filtrar solo registros con fechas válidas (no NaT)
                        mask_fecha_vencimiento = (
                            df_filtered["Fecha Vencimiento"].notna() &
                            (df_filtered["Fecha Vencimiento"] >= fecha_desde_dt) &
                            (df_filtered["Fecha Vencimiento"] <= fecha_hasta_dt)
                        )
                        df_filtered = df_filtered[mask_fecha_vencimiento]
                    else:
                        st.warning("⚠️ La fecha 'desde' de vencimiento no puede ser mayor que la fecha 'hasta'")

                st.divider()

                # Mostrar tabla filtrada
                st.subheader(f"✍🏼 Tareas ({len(df_filtered)} )")

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
                    from io import BytesIO
                    import pandas as pd

                    buffer = BytesIO()
                    # Asegurarse de que las columnas a descargar son las mostradas
                    df_to_download = df_filtered[columnas_disponibles]
                    df_to_download.to_excel(buffer, index=False, engine="openpyxl")
                    buffer.seek(0)

                    st.download_button(
                        label="📥 Descargar datos filtrados como Excel",
                        data=buffer.getvalue(),
                        file_name="tareas_clickup_filtradas.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

                    # Agregar gráficos interactivos
                    st.divider()

                    # Importar y mostrar gráficos
                    try:
                        from reportes.clickup_charts import clickup_charts

                        # Preparar rangos de fechas para pasar a gráficos
                        fecha_creacion_rango_param = None
                        if fecha_creacion_desde and fecha_creacion_hasta and fecha_creacion_desde <= fecha_creacion_hasta:
                            fecha_creacion_rango_param = (fecha_creacion_desde, fecha_creacion_hasta)
                        
                        fecha_cierre_rango_param = None
                        if fecha_cierre_desde and fecha_cierre_hasta and fecha_cierre_desde <= fecha_cierre_hasta:
                            fecha_cierre_rango_param = (fecha_cierre_desde, fecha_cierre_hasta)
                        
                        fecha_vencimiento_rango_param = None
                        if fecha_vencimiento_desde and fecha_vencimiento_hasta and fecha_vencimiento_desde <= fecha_vencimiento_hasta:
                            fecha_vencimiento_rango_param = (fecha_vencimiento_desde, fecha_vencimiento_hasta)

                        clickup_charts.mostrar_todos_los_graficos(
                            df_filtered, 
                            espacios_filtrados=espacios_selected if espacios_selected else None,
                            estados_filtrados=estados_selected if estados_selected else None,
                            etiquetas_filtradas=etiquetas_selected if etiquetas_selected else None,
                            fecha_creacion_rango=fecha_creacion_rango_param,
                            fecha_cierre_rango=fecha_cierre_rango_param,
                            fecha_vencimiento_rango=fecha_vencimiento_rango_param
                        )
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
