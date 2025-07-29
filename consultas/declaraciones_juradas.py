""" 
Módulo de consulta de declaraciones juradas
Maneja toda la lógica de la pestaña de declaraciones juradas
"""

import streamlit as st
from database import db_manager
from ui_components import ui_components
from config import TABS_CONFIG, MESSAGES


class ConsultaDeclaracionesJuradas:
    """Manejador de consultas de declaraciones juradas"""

    def __init__(self):
        self.config = TABS_CONFIG["declaraciones_juradas"]
        self.messages = MESSAGES

    def mostrar_interfaz(self):
        """Muestra la interfaz de consulta de declaraciones juradas"""
        st.header(self.config["header"])
        st.write(self.config["description"])

        # Crear formulario con múltiples campos SIEMPRE arriba
        with st.form("consulta_declaraciones_form"):
            col1, col2 = st.columns(2)

            with col1:
                # Campo para CUIT
                cuit_input = st.text_input(
                    "CUIT (podés poner más de 1 es opcional):",
                    placeholder="Ej: 20123456781, 27987654329",
                    help="Ingresá los números de CUIT separados por coma"
                )

                # Campo para cuenta
                cuenta_input = st.text_input(
                    "Cuenta (podés poner más de 1 es opcional):",
                    placeholder="Ej: 123456, 789012",
                    help="Ingresá los números de cuenta separados por coma"
                )

            with col2:
                # Campo para ID simplificado
                id_simplificado_input = st.text_input(
                    "ID Simplificado (podés poner más de 1 es opcional):",
                    placeholder="Ej: 1001, 1002, 1003",
                    help="Ingresá los IDs simplificados separados por coma"
                )

            # Botón de búsqueda
            submitted = st.form_submit_button("🔍 Buscar Declaraciones Juradas", use_container_width=True)

        if submitted:
            self.procesar_busqueda(cuit_input, cuenta_input, id_simplificado_input)
        else:
            # Solo mostrar resultados persistentes si NO se envió una nueva búsqueda
            # Separador visual
            st.divider()
            # Restaurar resultados persistentes si existen
            ui_components.mostrar_resultados_persistentes(
                "declaraciones_juradas_consulta"
            )
            ui_components.mostrar_resultados_persistentes(
                "declaraciones_juradas_adicional"
            )

    def procesar_busqueda(self, cuit_input, cuenta_input, id_simplificado_input):
        """Procesa la búsqueda de declaraciones juradas"""
        try:
            # Separador visual para nueva búsqueda
            st.divider()

            # Verificar que al menos un campo haya sido ingresado
            campos = [cuit_input, cuenta_input, id_simplificado_input]

            if not ui_components.validar_campos_requeridos(campos):
                st.warning(self.messages["validation"]["min_one_field"])
                return

            # Construir condiciones WHERE dinámicamente
            conditions = []

            # Procesar CUIT
            if cuit_input.strip():
                cuits = [x.strip() for x in cuit_input.split(',') if x.strip().isdigit()]
                if cuits:
                    # n_cuit es char(11) - necesita comillas
                    cuits_quoted = [f"'{cuit}'" for cuit in cuits]
                    cuits_str = ','.join(cuits_quoted)
                    conditions.append(f"a.n_cuit IN ({cuits_str})")

            # Procesar cuenta
            if cuenta_input.strip():
                cuentas = [x.strip() for x in cuenta_input.split(',') if x.strip().isdigit()]
                if cuentas:
                    # c_cuenta es integer - NO necesita comillas
                    cuentas_str = ','.join(cuentas)
                    conditions.append(f"a.c_cuenta IN ({cuentas_str})")

            # Procesar ID simplificado
            if id_simplificado_input.strip():
                ids = [x.strip() for x in id_simplificado_input.split(',') if x.strip().isdigit()]
                if ids:
                    # id_simplificado es integer - NO necesita comillas
                    ids_str = ','.join(ids)
                    conditions.append(f"a.id_simplificado IN ({ids_str})")

            if not conditions:
                st.warning("⚠️ Ingresá al menos un criterio de búsqueda válido.")
                return

            # Mostrar criterios de búsqueda
            criterios = []
            if cuit_input.strip():
                criterios.append(f"CUIT: {cuit_input.strip()}")
            if cuenta_input.strip():
                criterios.append(f"Cuenta: {cuenta_input.strip()}")
            if id_simplificado_input.strip():
                criterios.append(f"ID Simplificado: {id_simplificado_input.strip()}")

            ui_components.mostrar_criterios_busqueda(
                criterios,
                "🔍 Buscando declaraciones juradas con criterios",
                "declaraciones_juradas_consulta",
            )

            # Crear controles de búsqueda
            spinner_container, cancel_container, cancel_key = ui_components.crear_controles_busqueda("declaraciones")

            # Mostrar botón de cancelar
            ui_components.mostrar_boton_cancelar(cancel_container, "declaraciones")
            st.subheader("📋 Resultados - Datos principales de declaraciones juradas ")
            # Ejecutar consulta principal
            def consulta_declaraciones():
                return db_manager.consultar_declaraciones_juradas(conditions)

            df = ui_components.ejecutar_con_spinner(
                spinner_container,
                "🔍 Consultando declaraciones juradas... Presioná 'Cancelar Búsqueda' si querés detener.",
                consulta_declaraciones
            )

            # Limpiar controles
            ui_components.limpiar_controles(spinner_container, cancel_container, cancel_key)

            # Validación robusta de resultados para consulta principal
            if df is None or df.empty:
                st.info(
                    "ℹ️ No se encontraron resultados para los criterios especificados."
                )
            else:
                columnas_metricas = {
                    "total": "Total registros",
                    "cuit": "CUITs únicos",
                    "cuenta": "Cuentas únicas"
                }
                columnas_validas = [
                    col
                    for col in columnas_metricas
                    if col in df.columns or col == "total"
                ]
                if columnas_validas:
                    ui_components.mostrar_estadisticas_basicas(
                        df, {k: columnas_metricas[k] for k in columnas_validas}
                    )
                ui_components.mostrar_resultados(df, "declaraciones_juradas_consulta")

            # Ejecutar consulta adicional
            st.subheader("📋 Resultados - Detalle de declaraciones juradas ")

            # Crear nuevos controles para la consulta adicional
            spinner_container_2, cancel_container_2, cancel_key_2 = ui_components.crear_controles_busqueda("declaraciones_adicional")

            ui_components.mostrar_boton_cancelar(cancel_container_2, "declaraciones_adicional")

            def consulta_declaraciones_adicional():
                return db_manager.consultar_declaraciones_juradas_adicional(conditions)

            df_adicional = ui_components.ejecutar_con_spinner(
                spinner_container_2,
                "🔍 Consultando declaraciones juradas (adicional)... Presioná 'Cancelar Búsqueda' si querés detener.",
                consulta_declaraciones_adicional
            )

            # Limpiar controles adicionales
            ui_components.limpiar_controles(spinner_container_2, cancel_container_2, cancel_key_2)

            # Validación robusta de resultados para consulta adicional
            if df_adicional is None or df_adicional.empty:
                st.info("ℹ️ No se encontraron resultados en la consulta adicional.")
            else:
                columnas_metricas_adicional = {
                    "total": "Total registros",
                    "cuit": "CUITs únicos",
                    "cuenta": "Cuentas únicas"
                }
                columnas_validas_adicional = [
                    col
                    for col in columnas_metricas_adicional
                    if col in df_adicional.columns or col == "total"
                ]
                if columnas_validas_adicional:
                    ui_components.mostrar_estadisticas_basicas(
                        df_adicional,
                        {
                            k: columnas_metricas_adicional[k]
                            for k in columnas_validas_adicional
                        },
                    )
                ui_components.mostrar_resultados(
                    df_adicional, "declaraciones_juradas_adicional"
                )
        except Exception as e:
            st.error(self.messages["errors"]["database_error"].format(error=e))


# Instancia global de consulta de declaraciones juradas
consulta_declaraciones_juradas = ConsultaDeclaracionesJuradas()
