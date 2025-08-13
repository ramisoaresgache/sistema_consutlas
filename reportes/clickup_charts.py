
"""
Módulo para generar gráficos de ClickUp
Maneja la creación de visualizaciones interactivas
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

class ClickUpCharts:
    """Generador de gráficos para datos de ClickUp"""
    
    def __init__(self):
        self.color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    
    def _generar_titulo_filtrado(self, titulo_base, espacios_filtrados=None, estados_filtrados=None, etiquetas_filtradas=None, fecha_creacion_rango=None, fecha_cierre_rango=None, fecha_vencimiento_rango=None):
        """Genera un título dinámico basado en los filtros aplicados"""
        filtros_activos = []
        
        if espacios_filtrados:
            if len(espacios_filtrados) == 1:
                filtros_activos.append(f"Espacio: {espacios_filtrados[0]}")
            elif len(espacios_filtrados) <= 3:
                filtros_activos.append(f"Espacios: {', '.join(espacios_filtrados)}")
            else:
                filtros_activos.append(f"Espacios: {len(espacios_filtrados)} seleccionados")
        
        if estados_filtrados:
            if len(estados_filtrados) == 1:
                filtros_activos.append(f"Estado: {estados_filtrados[0]}")
            elif len(estados_filtrados) <= 3:
                filtros_activos.append(f"Estados: {', '.join(estados_filtrados)}")
            else:
                filtros_activos.append(f"Estados: {len(estados_filtrados)} seleccionados")
        
        if etiquetas_filtradas:
            if len(etiquetas_filtradas) == 1:
                filtros_activos.append(f"Etiqueta: {etiquetas_filtradas[0]}")
            elif len(etiquetas_filtradas) <= 3:
                filtros_activos.append(f"Etiquetas: {', '.join(etiquetas_filtradas)}")
            else:
                filtros_activos.append(f"Etiquetas: {len(etiquetas_filtradas)} seleccionadas")
        
        if fecha_creacion_rango and len(fecha_creacion_rango) == 2:
            desde, hasta = fecha_creacion_rango
            filtros_activos.append(f"Creación: {desde} - {hasta}")
        
        if fecha_cierre_rango and len(fecha_cierre_rango) == 2:
            desde, hasta = fecha_cierre_rango
            filtros_activos.append(f"Cierre: {desde} - {hasta}")
        
        if fecha_vencimiento_rango and len(fecha_vencimiento_rango) == 2:
            desde, hasta = fecha_vencimiento_rango
            filtros_activos.append(f"Vencimiento: {desde} - {hasta}")
        
        titulo = titulo_base
        if filtros_activos:
            filtros_texto = " | ".join(filtros_activos)
            titulo += f"<br><sub>{filtros_texto}</sub>"
        
        return titulo
    
    def grafico_torta_espacios(self, df, espacios_filtrados=None, estados_filtrados=None, etiquetas_filtradas=None, fecha_creacion_rango=None, fecha_cierre_rango=None, fecha_vencimiento_rango=None):
        """Gráfico de torta: distribución de tareas por espacio"""
        if df.empty:
            st.warning("No hay datos para mostrar el gráfico de espacios")
            return
        
        # Contar tareas por espacio
        espacio_counts = df['Espacio'].value_counts()
        
        # Generar título dinámico
        titulo = self._generar_titulo_filtrado(
            "📊 Distribución de Tareas por Espacio",
            espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango
        )
        
        fig = px.pie(
            values=espacio_counts.values,
            names=espacio_counts.index,
            title=titulo,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>' +
                         'Tareas: %{value}<br>' +
                         'Porcentaje: %{percent}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            showlegend=True,
            font=dict(size=12)
        )
        
        return fig
    
    def grafico_lineas_fechas(self, df, espacios_filtrados=None, estados_filtrados=None, etiquetas_filtradas=None, fecha_creacion_rango=None, fecha_cierre_rango=None, fecha_vencimiento_rango=None):
        """Gráfico de líneas: tareas creadas por fecha"""
        if df.empty:
            st.warning("No hay datos para mostrar el gráfico de fechas")
            return
        
        # Filtrar datos con fecha de creación válida
        df_fechas = df[df['Fecha Creación'].notna()].copy()
        
        if df_fechas.empty:
            st.warning("No hay tareas con fechas de creación válidas")
            return
        
        # Agrupar por fecha de creación
        df_fechas['Fecha'] = df_fechas['Fecha Creación'].dt.date
        fechas_counts = df_fechas.groupby('Fecha').size().reset_index(name='Cantidad')
        fechas_counts = fechas_counts.sort_values('Fecha')
        
        # Generar título dinámico
        titulo = self._generar_titulo_filtrado(
            "📈 Tareas Creadas por Fecha",
            espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango
        )
        
        fig = px.line(
            fechas_counts,
            x='Fecha',
            y='Cantidad',
            title=titulo,
            markers=True
        )
        
        fig.update_traces(
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8, color='#ff7f0e'),
            hovertemplate='<b>Fecha:</b> %{x}<br>' +
                         '<b>Tareas creadas:</b> %{y}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Fecha de Creación",
            yaxis_title="Número de Tareas",
            font=dict(size=12),
            hovermode='x unified'
        )
        
        return fig
    
    def grafico_barras_estados(self, df, espacios_filtrados=None, estados_filtrados=None, etiquetas_filtradas=None, fecha_creacion_rango=None, fecha_cierre_rango=None, fecha_vencimiento_rango=None):
        """Gráfico de barras: distribución de tareas por estado"""
        if df.empty:
            st.warning("No hay datos para mostrar el gráfico de estados")
            return
        
        # Contar tareas por estado
        estado_counts = df['Estado'].value_counts()
        
        # Generar título dinámico
        titulo = self._generar_titulo_filtrado(
            "📊 Distribución de Tareas por Estado",
            espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango
        )
        
        fig = px.bar(
            x=estado_counts.index,
            y=estado_counts.values,
            title=titulo,
            color=estado_counts.values,
            color_continuous_scale='viridis'
        )
        
        fig.update_traces(
            hovertemplate='<b>Estado:</b> %{x}<br>' +
                         '<b>Cantidad:</b> %{y}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Estado",
            yaxis_title="Número de Tareas",
            font=dict(size=12),
            showlegend=False
        )
        
        # Rotar etiquetas del eje X si son muy largas
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def grafico_columnas_asignados(self, df, espacios_filtrados=None, estados_filtrados=None, etiquetas_filtradas=None, fecha_creacion_rango=None, fecha_cierre_rango=None, fecha_vencimiento_rango=None):
        """Gráfico de columnas apiladas: tareas por asignado"""
        if df.empty:
            st.warning("No hay datos para mostrar el gráfico de asignados")
            return
        
        # Preparar datos de asignados
        asignados_data = []
        
        for idx, row in df.iterrows():
            task_id = row['ID']
            asignados_str = row['Asignados']
            
            if asignados_str and asignados_str.strip():
                # Dividir los asignados por coma
                asignados_list = [a.strip() for a in asignados_str.split(',')]
                for asignado in asignados_list:
                    if asignado:  # Solo si no está vacío
                        asignados_data.append({
                            'ID_Tarea': task_id,
                            'Asignado': asignado,
                            'Espacio': row['Espacio'],
                            'Estado': row['Estado']
                        })
            else:
                # Tarea sin asignados
                asignados_data.append({
                    'ID_Tarea': task_id,
                    'Asignado': 'Sin asignar',
                    'Espacio': row['Espacio'],
                    'Estado': row['Estado']
                })
        
        if not asignados_data:
            st.warning("No hay datos de asignaciones para mostrar")
            return
        
        df_asignados = pd.DataFrame(asignados_data)
        
        # Contar asignaciones por persona y espacio
        pivot_data = df_asignados.groupby(['Asignado', 'Espacio']).size().reset_index(name='Cantidad')
        
        # Generar título dinámico
        titulo = self._generar_titulo_filtrado(
            "👥 Distribución de Tareas por Asignado y Espacio",
            espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango
        )
        
        fig = px.bar(
            pivot_data,
            x='Asignado',
            y='Cantidad',
            color='Espacio',
            title=titulo,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_traces(
            hovertemplate='<b>Asignado:</b> %{x}<br>' +
                         '<b>Espacio:</b> %{legendgroup}<br>' +
                         '<b>Tareas:</b> %{y}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Asignado",
            yaxis_title="Número de Tareas",
            font=dict(size=12),
            legend_title="Espacio"
        )
        
        # Rotar etiquetas del eje X
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def grafico_barras_fechas_agentes(self, df, espacios_filtrados=None, estados_filtrados=None, etiquetas_filtradas=None, fecha_creacion_rango=None, fecha_cierre_rango=None, fecha_vencimiento_rango=None):
        """Gráfico de barras apiladas: comparación de fechas de creación y cierre por agente"""
        if df.empty:
            st.warning("No hay datos para mostrar el gráfico de fechas por agente")
            return
        
        # Preparar datos de agentes con fechas
        fechas_data = []
        
        for idx, row in df.iterrows():
            task_id = row['ID']
            asignados_str = row['Asignados']
            fecha_creacion = row['Fecha Creación']
            fecha_cierre = row['Fecha Cierre']
            
            if asignados_str and asignados_str.strip():
                # Dividir los asignados por coma
                asignados_list = [a.strip() for a in asignados_str.split(',')]
                for asignado in asignados_list:
                    if asignado:  # Solo si no está vacío
                        # Agregar fecha de creación - validar que no sea NaT
                        if pd.notna(fecha_creacion):
                            fechas_data.append({
                                'Agente': asignado,
                                'Fecha': fecha_creacion.strftime('%Y-%m-%d'),
                                'Tipo': 'Creación',
                                'Valor': 1
                            })
                        
                        # Agregar fecha de cierre - validar que no sea NaT
                        if pd.notna(fecha_cierre):
                            fechas_data.append({
                                'Agente': asignado,
                                'Fecha': fecha_cierre.strftime('%Y-%m-%d'),
                                'Tipo': 'Cierre',
                                'Valor': 1
                            })
            else:
                # Tarea sin asignados
                agente = 'Sin asignar'
                
                # Agregar fecha de creación - validar que no sea NaT
                if pd.notna(fecha_creacion):
                    fechas_data.append({
                        'Agente': agente,
                        'Fecha': fecha_creacion.strftime('%Y-%m-%d'),
                        'Tipo': 'Creación',
                        'Valor': 1
                    })
                
                # Agregar fecha de cierre - validar que no sea NaT
                if pd.notna(fecha_cierre):
                    fechas_data.append({
                        'Agente': agente,
                        'Fecha': fecha_cierre.strftime('%Y-%m-%d'),
                        'Tipo': 'Cierre',
                        'Valor': 1
                    })
        
        if not fechas_data:
            st.warning("No hay datos de fechas para mostrar")
            return
        
        df_fechas = pd.DataFrame(fechas_data)
        
        # Agrupar por agente y tipo de fecha
        pivot_data = df_fechas.groupby(['Agente', 'Tipo']).size().reset_index(name='Cantidad')
        
        # Generar título dinámico
        titulo = self._generar_titulo_filtrado(
            "📅 Comparación de Fechas de Creación vs Cierre por Agente",
            espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango
        )
        
        fig = px.bar(
            pivot_data,
            x='Agente',
            y='Cantidad',
            color='Tipo',
            title=titulo,
            color_discrete_map={
                'Creación': '#2E86AB',  # Azul
                'Cierre': '#A23B72'     # Púrpura
            },
            barmode='group'  # Barras agrupadas en lugar de apiladas
        )
        
        fig.update_traces(
            hovertemplate='<b>Agente:</b> %{x}<br>' +
                         '<b>Tipo:</b> %{legendgroup}<br>' +
                         '<b>Cantidad:</b> %{y}<br>' +
                         '<extra></extra>'
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Agente",
            yaxis_title="Cantidad de Tareas",
            font=dict(size=12),
            legend_title="Tipo de Fecha",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Rotar etiquetas del eje X
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    def mostrar_todos_los_graficos(self, df, espacios_filtrados=None, estados_filtrados=None, etiquetas_filtradas=None, fecha_creacion_rango=None, fecha_cierre_rango=None, fecha_vencimiento_rango=None):
        """Muestra todos los gráficos en la interfaz de Streamlit"""
        if df.empty:
            st.warning("No hay datos para mostrar gráficos")
            return
        
        st.subheader("📊 Análisis Visual de Tareas")
        
        # Mostrar información de filtros aplicados
        if espacios_filtrados or estados_filtrados or etiquetas_filtradas or fecha_creacion_rango or fecha_cierre_rango or fecha_vencimiento_rango:
            filtros_info = []
            if espacios_filtrados:
                filtros_info.append(f"**Espacios:** {', '.join(espacios_filtrados)}")
            if estados_filtrados:
                filtros_info.append(f"**Estados:** {', '.join(estados_filtrados)}")
            if etiquetas_filtradas:
                filtros_info.append(f"**Etiquetas:** {', '.join(etiquetas_filtradas)}")
            if fecha_creacion_rango and len(fecha_creacion_rango) == 2:
                desde, hasta = fecha_creacion_rango
                filtros_info.append(f"**Creación:** {desde} - {hasta}")
            if fecha_cierre_rango and len(fecha_cierre_rango) == 2:
                desde, hasta = fecha_cierre_rango
                filtros_info.append(f"**Cierre:** {desde} - {hasta}")
            if fecha_vencimiento_rango and len(fecha_vencimiento_rango) == 2:
                desde, hasta = fecha_vencimiento_rango
                filtros_info.append(f"**Vencimiento:** {desde} - {hasta}")
            
            if filtros_info:  # Solo mostrar si hay filtros activos
                st.info(f"🔍 **Filtros aplicados:** {' | '.join(filtros_info)}")
        
        # Crear pestañas para los gráficos
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🍰 Por Espacio",
            "📈 Por Fecha",
            "📊 Por Estado", 
            "👥 Por Asignado",
            "📅 Fechas vs Agentes"
        ])
        
        with tab1:
            st.markdown("### 🍰 Distribución de Tareas por Espacio")
            fig1 = self.grafico_torta_espacios(df, espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
        
        with tab2:
            st.markdown("### 📈 Evolución de Tareas Creadas")
            fig2 = self.grafico_lineas_fechas(df, espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            st.markdown("### 📊 Distribución por Estado")
            fig3 = self.grafico_barras_estados(df, espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango)
            if fig3:
                st.plotly_chart(fig3, use_container_width=True)
        
        with tab4:
            st.markdown("### 👥 Tareas por Asignado y Espacio")
            fig4 = self.grafico_columnas_asignados(df, espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango)
            if fig4:
                st.plotly_chart(fig4, use_container_width=True)
        
        with tab5:
            st.markdown("### 📅 Comparación de Fechas por Agente")
            fig5 = self.grafico_barras_fechas_agentes(df, espacios_filtrados, estados_filtrados, etiquetas_filtradas, fecha_creacion_rango, fecha_cierre_rango, fecha_vencimiento_rango)
            if fig5:
                st.plotly_chart(fig5, use_container_width=True)


# Instancia global del generador de gráficos
clickup_charts = ClickUpCharts()
