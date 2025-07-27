""" 
Módulo de consulta de planes de pago
Maneja toda la lógica de la pestaña de planes
"""

import streamlit as st
from database import db_manager
from ui_components import ui_components
from config import TABS_CONFIG, MESSAGES


class ConsultaPlanes:
    """Manejador de consultas de planes de pago"""

    def __init__(self):
        self.config = TABS_CONFIG["planes"]
        self.messages = MESSAGES

    def mostrar_interfaz(self):
        """Muestra la interfaz de consulta de planes"""
        st.header(self.config["header"])
        st.write(self.config["description"])
        
        # Mostrar resultados persistentes si existen (restauración automática)
        persistio = False
        persistio |= ui_components.mostrar_resultados_persistentes("planes_consulta")
        persistio |= ui_components.mostrar_resultados_persistentes("planes_transacciones_consulta")

        # Crear formulario
        with st.form("consulta_planes_form"):
            col1, col2 = st.columns(2)
            with col1:
                plan_input = st.text_input(
                    "Plan (OBLIGATORIO) 🔴:",
                    placeholder="Ej: 122250",
                    help="⚠️ Este campo es obligatorio. Ingresá el número de plan a consultar."
                )
            with col2:
                cuota_input = st.text_input(
                    "Cuota (opcional):",
                    placeholder="Ej: 1, 2, 3",
                    help="Filtrá por cuota específica. Dejá en blanco para ver todas las cuotas."
                )
            submitted = st.form_submit_button("🔍 Buscar Plan", use_container_width=True)

        if submitted:
            self.procesar_busqueda(plan_input, cuota_input)

    def procesar_busqueda(self, plan_input, cuota_input):
        """Procesa la búsqueda de planes"""
        try:
            # Verificar que el campo plan haya sido ingresado
            if not plan_input.strip():
                st.warning("⚠️ El campo Plan es obligatorio.")
                return
            
            # Validar que sea un número
            if not plan_input.strip().isdigit():
                st.warning("⚠️ El plan debe ser un número válido.")
                return

            # Validar cuota si se ingresó
            if cuota_input.strip() and not cuota_input.strip().isdigit():
                st.warning("⚠️ La cuota debe ser un número válido.")
                return

            # Construir condiciones WHERE
            conditions = [f"a.n_plan = {plan_input.strip()}"]
            
            # Agregar filtro de cuota si se especificó
            if cuota_input.strip():
                conditions.append(f"b.n_cuota_plan = {cuota_input.strip()}")
            
            plan_condition = " AND ".join(conditions)

            # Mostrar criterios de búsqueda
            criterios = [f"🎯 Plan: {plan_input.strip()}"]
            if cuota_input.strip():
                criterios.append(f"Cuota: {cuota_input.strip()}")
            ui_components.mostrar_criterios_busqueda(criterios, "🔍 Consultando plan de pago")

            # ===================
            # CONSULTA 1: DETALLES DEL PLAN
            # ===================
            st.subheader("📋 Resultados - Detalles del Plan")
            
            # Crear controles para la primera consulta
            spinner_container_1, cancel_container_1, cancel_key_1 = ui_components.crear_controles_busqueda("planes_detalles")
            ui_components.mostrar_boton_cancelar(cancel_container_1, "planes_detalles")
            
            def consulta_planes():
                return db_manager.consultar_planes(plan_condition)
            
            df_planes = ui_components.ejecutar_con_spinner(
                spinner_container_1,
                "🔍 Consultando detalles del plan... Presioná 'Cancelar Búsqueda' si querés detener.",
                consulta_planes
            )
            
            # Limpiar controles
            ui_components.limpiar_controles(spinner_container_1, cancel_container_1, cancel_key_1)
            
            if df_planes is not None and len(df_planes) > 0:
                # Mostrar estadísticas básicas
                columnas_metricas_planes = {
                    "total": "Total cuotas",
                    "plan": "Planes únicos"
                }
                ui_components.mostrar_estadisticas_basicas(df_planes, columnas_metricas_planes)
                
                # Mostrar resultados
                ui_components.mostrar_resultados(df_planes, "planes_consulta")
            else:
                st.info("ℹ️ No se encontraron detalles para el plan especificado.")

            # ===================
            # CONSULTA 2: TRANSACCIONES DEL PLAN
            # ===================
            st.subheader("💳 Resultados - Detalles de cuotas del Plan")
            
            # Crear controles para la segunda consulta
            spinner_container_2, cancel_container_2, cancel_key_2 = ui_components.crear_controles_busqueda("planes_transacciones")
            ui_components.mostrar_boton_cancelar(cancel_container_2, "planes_transacciones")
            
            def consulta_planes_transacciones():
                return db_manager.consultar_planes_transacciones(plan_condition)
            
            df_transacciones = ui_components.ejecutar_con_spinner(
                spinner_container_2,
                "🔍 Consultando transacciones del plan... Presioná 'Cancelar Búsqueda' si querés detener.",
                consulta_planes_transacciones
            )
            
            # Limpiar controles
            ui_components.limpiar_controles(spinner_container_2, cancel_container_2, cancel_key_2)
            
            if df_transacciones is not None and len(df_transacciones) > 0:
                # Mostrar estadísticas básicas
                columnas_metricas_transacciones = {
                    "total": "Total registros",
                    "cuenta": "Cuentas únicas",
                    "transaccion": "Transacciones únicas",
                    "sistema": "Sistemas únicos"
                }
                ui_components.mostrar_estadisticas_basicas(df_transacciones, columnas_metricas_transacciones)
                
                # Mostrar resultados
                ui_components.mostrar_resultados(df_transacciones, "planes_transacciones_consulta")
            else:
                st.info("ℹ️ No se encontraron transacciones para el plan especificado.")

        except Exception as e:
            st.error(self.messages["errors"]["database_error"].format(error=e))


# Instancia global de consulta de planes
consulta_planes = ConsultaPlanes()
