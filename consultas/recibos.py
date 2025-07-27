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

        # Formulario para controlar el envío
        with st.form("consulta_recibos_form"):
            # Entrada de comprobantes
            comprobantes_input = st.text_input(
                "Número/s de comprobante/s (podes poner mas de 1 es opcional):",
                placeholder="Ej: 123456, 789012, 345678",
                help="Ingresá los números de comprobante separados por coma",
            )

            # Botón de envío del formulario
            submitted = st.form_submit_button(
                "🔍 Buscar Recibos", use_container_width=True
            )

        # Procesar cuando se envía el formulario
        if submitted:
            self.procesar_busqueda(comprobantes_input)
        else:
            # Solo mostrar resultados persistentes si NO se envió una nueva búsqueda
            # Separador visual
            st.divider()
            # Restaurar resultados persistentes si existen
            ui_components.mostrar_resultados_persistentes("recibos_consulta")

    def procesar_busqueda(self, comprobantes_input):
        """Procesa la búsqueda de recibos"""
        try:
            # Separador visual para nueva búsqueda
            st.divider()

            # Procesar entrada
            comprobantes = [
                x.strip() for x in comprobantes_input.split(',') 
                if x.strip().isdigit()
            ]

            # Validar longitud máxima de comprobantes (máximo 16 dígitos)
            comprobantes_invalidos = [c for c in comprobantes if len(c) > 16]
            if comprobantes_invalidos:
                st.warning(
                    f"⚠️ Los siguientes comprobantes exceden el máximo de 16 dígitos: {', '.join(comprobantes_invalidos)}. Por favor corregí la entrada."
                )
                return

            if not comprobantes:
                st.warning(self.messages["validation"]["min_one_comprobante"])
                return

            # Mostrar información de la búsqueda con limpieza de resultados anteriores
            comprobantes_texto = ', '.join(comprobantes[:5])
            if len(comprobantes) > 5:
                comprobantes_texto += "..."

            criterios = [
                f"Comprobantes: {comprobantes_texto}",
                f"Total: {len(comprobantes)}",
            ]
            ui_components.mostrar_criterios_busqueda(
                criterios, "🔍 Buscando recibos con criterios", "recibos_consulta"
            )

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

            # Validación robusta de resultados
            if df is None or df.empty:
                st.info(
                    "ℹ️ No se encontraron resultados para los comprobantes ingresados."
                )
                return

            # Validar que las columnas esperadas existen antes de mostrar métricas
            columnas_metricas = {
                "total": "Total registros",
                "comprobante": "Comprobantes únicos",
            }
            columnas_validas = [
                col for col in columnas_metricas if col in df.columns or col == "total"
            ]
            if columnas_validas:
                ui_components.mostrar_estadisticas_basicas(
                    df, {k: columnas_metricas[k] for k in columnas_validas}
                )

            # Mostrar resultados
            ui_components.mostrar_resultados(df, "recibos_consulta")
        except Exception as e:
            st.error(self.messages["errors"]["database_error"].format(error=e))


# Instancia global de consulta de recibos
consulta_recibos = ConsultaRecibos()
