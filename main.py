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

        # SUB-PESTAÑA 2: CONSULTA DE LOTES BANCARIOS Y DE LAS CAJAS
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
                        # Importar datetime como dt para evitar conflictos
                        from datetime import datetime as dt

                        # Convertir las fechas a datetime para comparación segura
                        fecha_desde_dt = dt.combine(fecha_creacion_desde, dt.min.time())
                        fecha_hasta_dt = dt.combine(fecha_creacion_hasta, dt.max.time())

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
                        # Importar datetime como dt para evitar conflictos
                        from datetime import datetime as dt

                        # Convertir las fechas a datetime para comparación segura
                        fecha_desde_dt = dt.combine(fecha_cierre_desde, dt.min.time())
                        fecha_hasta_dt = dt.combine(fecha_cierre_hasta, dt.max.time())

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
                        # Importar datetime como dt para evitar conflictos
                        from datetime import datetime as dt

                        # Convertir las fechas a datetime para comparación segura
                        fecha_desde_dt = dt.combine(
                            fecha_vencimiento_desde, dt.min.time()
                        )
                        fecha_hasta_dt = dt.combine(
                            fecha_vencimiento_hasta, dt.max.time()
                        )

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

                    except Exception as e:
                        st.error(f"❌ Error al preparar descarga: {str(e)}")

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
            st.subheader("📊 Reportes Estadísticos de Recaudación")

            # Inputs de periodo
            col_a, col_b, col_btn = st.columns([1, 1, 1])
            with col_a:
                ano_sel = st.number_input("Año", min_value=2000, max_value=2100, value=2025, step=1)
            with col_b:
                cuota_sel = st.number_input("Cuota", min_value=1, max_value=99, value=8, step=1)
            with col_btn:
                consultar = st.button("🔎 Consultar", use_container_width=True)

            if consultar:
                try:
                    from database import db_manager
                    import importlib
                    px = importlib.import_module("plotly.express")

                    def formato_moneda(valor: float) -> str:
                        base = f"{valor:,.2f}"
                        return base.replace(",", "X").replace(".", ",").replace("X", ".")

                    # Solo ejecutar consultas básicas al inicio
                    # Ejecutar consulta para obtener total de deuda
                    df_total_deuda = db_manager.consultar_estadisticas_total_deuda(int(ano_sel), int(cuota_sel))
                    total_deuda = 0.0
                    if df_total_deuda is not None and not df_total_deuda.empty and "total_deuda" in df_total_deuda.columns:
                        total_deuda = float(df_total_deuda["total_deuda"].iloc[0])

                    # Obtener datos por localidad (primero intentamos el método directo)
                    df_por_localidad = db_manager.consultar_estadisticas_por_localidad_directo(int(ano_sel), int(cuota_sel))
                    
                    # Si falla el método directo, intentamos con tabla temporal
                    if df_por_localidad is None or df_por_localidad.empty:
                        temp_created = db_manager.crear_temp_emitido_por_zona(int(ano_sel), int(cuota_sel))
                        if temp_created:
                            df_por_localidad = db_manager.consultar_estadisticas_por_localidad()
                        else:
                            st.warning("⚠️ No se pudieron obtener datos por localidad usando tabla temporal.")

                    # Guardar datos básicos en session_state para preservar entre recargas
                    st.session_state['estadisticas_data'] = {
                        'total_deuda': total_deuda,
                        'df_por_localidad': df_por_localidad,
                        'ano_sel': int(ano_sel),
                        'cuota_sel': int(cuota_sel)
                    }

                except Exception as e:
                    st.error(f"❌ Error ejecutando consulta: {e}")

            # Mostrar resultados si hay datos en session_state
            if 'estadisticas_data' in st.session_state:
                data = st.session_state['estadisticas_data']
                
                def formato_moneda(valor: float) -> str:
                    base = f"{valor:,.2f}"
                    return base.replace(",", "X").replace(".", ",").replace("X", ".")

                # Mostrar métrica principal
                st.metric("💳 Total Deuda", f"$ {formato_moneda(data['total_deuda'])}")

                st.divider()

                # Crear tabs para diferentes vistas
                tab1, tab2, tab3, tab4 = st.tabs(["📍 Deuda por Localidad", "✅ Pagos Confirmados", "⏳ Pagos sin Imputar", "⚠️ Deudores"])
                
                with tab1:
                    # Mostrar tabla de datos por localidad
                    if data['df_por_localidad'] is not None and not data['df_por_localidad'].empty:
                        st.subheader("📍 Deuda por Localidad")
                        st.dataframe(data['df_por_localidad'], use_container_width=True, height=400)

                        # Gráfico de barras por localidad
                        if "d_localidad" in data['df_por_localidad'].columns and "capital_total" in data['df_por_localidad'].columns:
                            import importlib
                            px = importlib.import_module("plotly.express")
                            
                            fig_bar = px.bar(
                                data['df_por_localidad'],
                                x="d_localidad",
                                y="capital_total",
                                title="Deuda por Localidad",
                                labels={"d_localidad": "Localidad", "capital_total": "Capital Total"}
                            )
                            fig_bar.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig_bar, use_container_width=True)

                            # Gráfico de torta
                            fig_pie = px.pie(
                                data['df_por_localidad'],
                                names="d_localidad",
                                values="capital_total",
                                title="Distribución de Deuda por Localidad"
                            )
                            st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("ℹ️ No se encontraron datos por localidad para el período seleccionado.")

                with tab2:
                    # Ejecutar consulta de pagos confirmados solo cuando se accede a esta tab
                    if st.button("🔄 Cargar Pagos Confirmados", use_container_width=True):
                        with st.spinner("Cargando pagos confirmados..."):
                            from database import db_manager
                            
                            # Consulta total
                            df_pagos_confirmados_total = db_manager.consultar_estadisticas_pagos_confirmados_total(data['ano_sel'], data['cuota_sel'])
                            total_confirmados = 0.0
                            cantidad_confirmados = 0
                            if df_pagos_confirmados_total is not None and not df_pagos_confirmados_total.empty:
                                if "total_confirmados" in df_pagos_confirmados_total.columns:
                                    total_confirmados = float(df_pagos_confirmados_total["total_confirmados"].iloc[0]) if df_pagos_confirmados_total["total_confirmados"].iloc[0] is not None else 0.0
                                if "cantidad_registros" in df_pagos_confirmados_total.columns:
                                    cantidad_confirmados = int(df_pagos_confirmados_total["cantidad_registros"].iloc[0]) if df_pagos_confirmados_total["cantidad_registros"].iloc[0] is not None else 0
                            
                            # Consulta detalle
                            df_pagos_confirmados_detalle = db_manager.consultar_estadisticas_pagos_confirmados_detalle(data['ano_sel'], data['cuota_sel'])
                            
                            # Guardar en session_state
                            st.session_state['pagos_confirmados'] = {
                                'total': total_confirmados,
                                'cantidad': cantidad_confirmados,
                                'detalle': df_pagos_confirmados_detalle
                            }
                    
                    # Mostrar datos si están disponibles
                    if 'pagos_confirmados' in st.session_state:
                        pag_conf = st.session_state['pagos_confirmados']
                        
                        # Mostrar métricas
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("✅ Total Confirmados", f"$ {formato_moneda(pag_conf['total'])}")
                        with col2:
                            st.metric("📊 Registros", f"{pag_conf['cantidad']}")
                        
                        # Mostrar datos de pagos confirmados
                        if pag_conf['detalle'] is not None and not pag_conf['detalle'].empty:
                            st.subheader("✅ Pagos Confirmados - Detalle")
                            st.dataframe(pag_conf['detalle'], use_container_width=True, height=400)
                        else:
                            st.info("ℹ️ No se encontraron pagos confirmados para el período seleccionado.")

                with tab3:
                    # Ejecutar consulta de pagos sin imputar solo cuando se accede a esta tab
                    if st.button("🔄 Cargar Pagos Sin Imputar", use_container_width=True):
                        with st.spinner("Cargando pagos sin imputar..."):
                            from database import db_manager
                            
                            # Consulta total
                            df_pagos_sin_imputar_total = db_manager.consultar_estadisticas_pagos_sin_imputar_total(data['ano_sel'], data['cuota_sel'])
                            total_sin_imputar = 0.0
                            cantidad_sin_imputar = 0
                            if df_pagos_sin_imputar_total is not None and not df_pagos_sin_imputar_total.empty:
                                if "total_sin_imputar" in df_pagos_sin_imputar_total.columns:
                                    total_sin_imputar = float(df_pagos_sin_imputar_total["total_sin_imputar"].iloc[0]) if df_pagos_sin_imputar_total["total_sin_imputar"].iloc[0] is not None else 0.0
                                if "cantidad_registros" in df_pagos_sin_imputar_total.columns:
                                    cantidad_sin_imputar = int(df_pagos_sin_imputar_total["cantidad_registros"].iloc[0]) if df_pagos_sin_imputar_total["cantidad_registros"].iloc[0] is not None else 0
                            
                            # Consulta detalle
                            df_pagos_sin_imputar_detalle = db_manager.consultar_estadisticas_pagos_sin_imputar_detalle(data['ano_sel'], data['cuota_sel'])
                            
                            # Guardar en session_state
                            st.session_state['pagos_sin_imputar'] = {
                                'total': total_sin_imputar,
                                'cantidad': cantidad_sin_imputar,
                                'detalle': df_pagos_sin_imputar_detalle
                            }
                    
                    # Mostrar datos si están disponibles
                    if 'pagos_sin_imputar' in st.session_state:
                        pag_sin_imp = st.session_state['pagos_sin_imputar']
                        
                        # Mostrar métricas
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("⏳ Total Sin Imputar", f"$ {formato_moneda(pag_sin_imp['total'])}")
                        with col2:
                            st.metric("📊 Registros", f"{pag_sin_imp['cantidad']}")
                        
                        # Mostrar datos de pagos sin imputar
                        if pag_sin_imp['detalle'] is not None and not pag_sin_imp['detalle'].empty:
                            st.subheader("⏳ Pagos Sin Imputar - Detalle")
                            st.dataframe(pag_sin_imp['detalle'], use_container_width=True, height=400)
                            
                            # Botón de descarga de Excel para pagos sin imputar
                            from io import BytesIO
                            buffer = BytesIO()
                            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                                pag_sin_imp['detalle'].to_excel(writer, index=False, sheet_name="Pagos_Sin_Imputar")
                            buffer.seek(0)
                            
                            st.download_button(
                                label="📊 Descargar Pagos Sin Imputar en Excel",
                                data=buffer.getvalue(),
                                file_name=f"pagos_sin_imputar_{data['ano_sel']}_cuota_{data['cuota_sel']}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_pagos_sin_imputar_{data['ano_sel']}_{data['cuota_sel']}"
                            )
                        else:
                            st.info("ℹ️ No se encontraron pagos sin imputar para el período seleccionado.")

                with tab4:
                    # Ejecutar consulta de deudores solo cuando se accede a esta tab
                    if st.button("🔄 Cargar Deudores", use_container_width=True):
                        with st.spinner("Cargando deudores..."):
                            from database import db_manager
                            
                            # Consulta total
                            df_pagos_deudores_total = db_manager.consultar_estadisticas_pagos_deudores_total(data['ano_sel'], data['cuota_sel'])
                            total_deudores = 0.0
                            cantidad_deudores = 0
                            if df_pagos_deudores_total is not None and not df_pagos_deudores_total.empty:
                                if "total_deudores" in df_pagos_deudores_total.columns:
                                    total_deudores = float(df_pagos_deudores_total["total_deudores"].iloc[0]) if df_pagos_deudores_total["total_deudores"].iloc[0] is not None else 0.0
                                if "cantidad_registros" in df_pagos_deudores_total.columns:
                                    cantidad_deudores = int(df_pagos_deudores_total["cantidad_registros"].iloc[0]) if df_pagos_deudores_total["cantidad_registros"].iloc[0] is not None else 0
                            
                            # Consulta detalle
                            df_pagos_deudores_detalle = db_manager.consultar_estadisticas_pagos_deudores_detalle(data['ano_sel'], data['cuota_sel'])
                            
                            # Guardar en session_state
                            st.session_state['pagos_deudores'] = {
                                'total': total_deudores,
                                'cantidad': cantidad_deudores,
                                'detalle': df_pagos_deudores_detalle
                            }
                    
                    # Mostrar datos si están disponibles
                    if 'pagos_deudores' in st.session_state:
                        pag_deudores = st.session_state['pagos_deudores']
                        
                        # Mostrar métricas
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("⚠️ Total Deudores", f"$ {formato_moneda(pag_deudores['total'])}")
                        with col2:
                            st.metric("📊 Registros", f"{pag_deudores['cantidad']}")
                        
                        # Mostrar datos de deudores
                        if pag_deudores['detalle'] is not None and not pag_deudores['detalle'].empty:
                            st.subheader("⚠️ Deudores - Detalle")
                            st.dataframe(pag_deudores['detalle'], use_container_width=True, height=400)
                        else:
                            st.info("ℹ️ No se encontraron registros de deudores para el período seleccionado.")

                # Descarga de datos completa solo si hay al menos los datos básicos
                if 'resultados_estadisticas' in st.session_state and st.session_state['resultados_estadisticas']['df_por_localidad'] is not None:
                    from io import BytesIO
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        # Datos básicos siempre disponibles
                        st.session_state['resultados_estadisticas']['df_por_localidad'].to_excel(writer, index=False, sheet_name="Deuda_por_Localidad")
                        
                        # Datos adicionales si están cargados
                        if 'pagos_sin_imputar' in st.session_state and st.session_state['pagos_sin_imputar']['detalle'] is not None:
                            st.session_state['pagos_sin_imputar']['detalle'].to_excel(writer, index=False, sheet_name="Pagos_sin_Imputar")
                        
                        if 'pagos_confirmados' in st.session_state and st.session_state['pagos_confirmados']['detalle'] is not None:
                            st.session_state['pagos_confirmados']['detalle'].to_excel(writer, index=False, sheet_name="Pagos_Confirmados")
                        
                        if 'pagos_deudores' in st.session_state and st.session_state['pagos_deudores']['detalle'] is not None:
                            st.session_state['pagos_deudores']['detalle'].to_excel(writer, index=False, sheet_name="Deudores")
                        
                        # Hoja de totales
                        totales_data = {
                            "Metric": ["Total Deuda"],
                            "Monto": [st.session_state['resultados_estadisticas']['total_deuda']]
                        }
                        
                        # Agregar otros totales si están disponibles
                        if 'pagos_sin_imputar' in st.session_state:
                            totales_data["Metric"].append("Pagos sin Imputar")
                            totales_data["Monto"].append(st.session_state['pagos_sin_imputar']['total'])
                            
                        if 'pagos_confirmados' in st.session_state:
                            totales_data["Metric"].append("Pagos Confirmados")
                            totales_data["Monto"].append(st.session_state['pagos_confirmados']['total'])
                            
                        if 'pagos_deudores' in st.session_state:
                            totales_data["Metric"].append("Deudores")
                            totales_data["Monto"].append(st.session_state['pagos_deudores']['total'])
                        
                        pd.DataFrame(totales_data).to_excel(writer, index=False, sheet_name="Totales")
                    
                    buffer.seek(0)
                    st.download_button(
                        label="📥 Descargar Excel (Completo)",
                        data=buffer.getvalue(),
                        file_name=f"estadisticas_completas_{data['ano_sel']}_{data['cuota_sel']}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
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
