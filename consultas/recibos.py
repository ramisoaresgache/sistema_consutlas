"""
Módulo de consulta de recibos
Maneja toda la lógica de la pestaña de recibos
"""

import streamlit as st
from database import db_manager
from ui_components import ui_components
from config import TABS_CONFIG, MESSAGES


class ConsultaRecibos:
    """Manejador de consultas de recibos"""

    def __init__(self):
        self.config = TABS_CONFIG["recibos"]
        self.messages = MESSAGES

    def mostrar_interfaz(self):
        """Muestra la interfaz de consulta de recibos"""
        st.header(self.config["header"])
        st.write(self.config["description"])

        # Restaurar resultados persistentes si existen
        ui_components.mostrar_resultados_persistentes("recibos_consulta")

        # Entrada de comprobantes
        comprobantes_input = st.text_input(
            "Número/s de comprobante/s (podes poner mas de 1 es opcional):",
            placeholder="Ej: 123456, 789012, 345678",
            help="Ingresá los números de comprobante separados por coma"
        )

        if st.button("🔍 Buscar Recibos", use_container_width=True):
            self.procesar_busqueda(comprobantes_input)

    def procesar_busqueda(self, comprobantes_input):
        """Procesa la búsqueda de recibos"""
        try:
            # Procesar entrada
            comprobantes = [
                x.strip() for x in comprobantes_input.split(',') 
                if x.strip().isdigit()
            ]

            if not comprobantes:
                st.warning(self.messages["validation"]["min_one_comprobante"])
                return

            # Mostrar información de la búsqueda
            comprobantes_texto = ', '.join(comprobantes[:5])
            if len(comprobantes) > 5:
                comprobantes_texto += "..."

            st.info(f"🔍 Buscando {len(comprobantes)} comprobante(s): {comprobantes_texto}")

            # Crear controles de búsqueda
            spinner_container, cancel_container, cancel_key = ui_components.crear_controles_busqueda("recibos")

            # Mostrar botón de cancelar
            ui_components.mostrar_boton_cancelar(cancel_container, "recibos")

            # Ejecutar consulta
            def consulta_recibos():
                return db_manager.consultar_recibos(comprobantes)

            df = ui_components.ejecutar_con_spinner(
                spinner_container,
                "🔄 Consultando base de datos... Presioná 'Cancelar Búsqueda' si querés detener.",
                consulta_recibos
            )

            # Limpiar controles
            ui_components.limpiar_controles(spinner_container, cancel_container, cancel_key)

            if df is not None:
                # Mostrar estadísticas básicas
                columnas_metricas = {
                    "total": "Total registros",
                    "comprobante": "Comprobantes únicos"
                }
                ui_components.mostrar_estadisticas_basicas(df, columnas_metricas)

                # Mostrar resultados
                ui_components.mostrar_resultados(df, "recibos_consulta")

        except Exception as e:
            st.error(self.messages["errors"]["database_error"].format(error=e))


# Instancia global de consulta de recibos
consulta_recibos = ConsultaRecibos()
