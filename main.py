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

    # Crear pestañas principales
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            TABS_CONFIG["recibos"]["name"],
            TABS_CONFIG["lotes"]["name"],
            TABS_CONFIG["cuenta_corriente"]["name"],
            TABS_CONFIG["declaraciones_juradas"]["name"]
        ]
    )

    # PESTAÑA 1: CONSULTA DE RECIBOS
    with tab1:
        consulta_recibos.mostrar_interfaz()

    # PESTAÑA 2: CONSULTA DE LOTES BANCARIOS
    with tab2:
        consulta_lotes_bancarios.mostrar_interfaz()

    # PESTAÑA 3: CONSULTA DE CUENTA CORRIENTE
    with tab3:
        consulta_cuenta_corriente.mostrar_interfaz()
    # PESTAÑA 4: CONSULTA DE DECLARACIONES JURADAS
    with tab4:
        consulta_declaraciones_juradas.mostrar_interfaz()
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666; font-size: 0.8rem;">'
        "🔍 Sistema de Consultas - Municipalidad de Vicente López"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
