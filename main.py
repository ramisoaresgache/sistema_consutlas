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

        # Mensaje temporal mientras se desarrollan los reportes
        st.info("🚧 **Próximamente tendrás información aquí**")

        st.markdown(
            """
        ### 📊 Reportes en Desarrollo
        
        En esta sección encontrarás:
        
        - 📈 **Reportes estadísticos** de recaudación
        - 📊 **Dashboards interactivos** con métricas
        - 📅 **Reportes programados** automáticos
        - 📋 **Análisis de tendencias** temporales
        - 💰 **Resúmenes ejecutivos** de gestión
        
        ---
        
        💡 **Sugerencias de reportes**: Si tenés ideas para reportes específicos que te gustaría ver, 
        contactá al equipo de desarrollo.
        """
        )

        # Placeholder para futuras funcionalidades
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
            #### 📊 Reportes Estadísticos
            *Próximamente*
            
            - Resúmenes por período
            - Comparativas anuales
            - Análisis de recaudación
            """
            )

        with col2:
            st.markdown(
                """
            #### 📈 Dashboards
            *Próximamente*
            
            - Métricas en tiempo real
            - Gráficos interactivos
            - KPIs principales
            """
            )

        with col3:
            st.markdown(
                """
            #### 📅 Programados
            *Próximamente*
            
            - Reportes automáticos
            - Envío por email
            - Alertas personalizadas
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
