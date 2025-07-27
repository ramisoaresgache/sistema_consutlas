"""
Módulo de consulta de cuenta corriente
Maneja toda la lógica de la pestaña de cuenta corriente
"""

import streamlit as st
from database import db_manager
from ui_components import ui_components
from config import TABS_CONFIG, MESSAGES


class ConsultaCuentaCorriente:
    """Manejador de consultas de cuenta corriente"""

    def __init__(self):
        self.config = TABS_CONFIG["cuenta_corriente"]
        self.messages = MESSAGES

    def mostrar_interfaz(self):
        """Muestra la interfaz de consulta de cuenta corriente"""
        st.header(self.config["header"])
        st.write(self.config["description"])

        # Restaurar resultados persistentes si existen
        ui_components.mostrar_resultados_persistentes("ctacte_consulta")

        # Crear formulario con múltiples campos
        with st.form("consulta_ctacte_form"):
            col1, col2 = st.columns(2)

            with col1:
                # Campo para cuenta
                cuenta_input = st.text_input(
                    "Cuenta* (OBLIGATORIO solo podes buscar de a 1):",
                    placeholder="Ej: 650581, 650582",
                    help="Ingresá los números de cuenta separados por coma",
                )

                # Campo para año
                ano_input = st.text_input(
                    "Año/s (podes poner mas de 1 es opcional):",
                    placeholder="Ej: 2023, 2024",
                    help="Seleccioná el año de consulta",
                )

                # Campo para cuota
                cuota_input = st.text_input(
                    "Cuota/s (podes poner mas de 1 es opcional):",
                    placeholder="Ej: 1, 2, 3",
                    help="Seleccioná el número de cuota",
                )

                # Campo para capital
                capital_input = st.text_input(
                    "Capital (pone un monto es opcional):",
                    placeholder="Ej: 10000.50",
                    help="Ingresá los montos de capital separados por coma",
                )

            with col2:
                # Campo para transacciones
                transacciones_input = st.text_input(
                    "Transaccion/es (podes poner mas de 1 es opcional):",
                    placeholder="Ej: 129249776, 129249777",
                    help="Ingresá los códigos de sistema separados por coma",
                )

                # Campo para tasa
                tasa_input = st.text_input(
                    "Tasa (podes poner mas de 1 es opcional):",
                    placeholder="Ej: 200, 300",
                    help="Ingresá los códigos de tasa separados por coma"
                )

                # Campo para comprobante
                comprob_input = st.text_input(
                    "Comprobante/s  (podes poner mas de 1 es opcional):",
                    placeholder="Ej: 10748765384,10748765789",
                    help="Ingresá los números de comprobante separados por coma"
                )

                # # campo para sistema
                # sistema_input = st.text_input(
                #     "Sistema (opcional):",
                #     placeholder="Ej: 1 ",
                #     help="Ingresá el código de sistema",
                # )

            # Botón de búsqueda
            submitted_ctacte = st.form_submit_button("🔍 Buscar en Cta Cte", use_container_width=True)

        if submitted_ctacte:
            self.procesar_busqueda(
                cuenta_input,
                ano_input,
                cuota_input,
                capital_input,
                transacciones_input,
                tasa_input,
                comprob_input,
                # sistema_input,
            )

    def procesar_busqueda(
        self,
        cuenta_input,
        ano_input,
        cuota_input,
        capital_input,
        transacciones_input,
        tasa_input,
        comprob_input,
        # sistema_input,
    ):
        """Procesa la búsqueda de cuenta corriente"""
        try:
            # Verificar que el campo cuenta (obligatorio) haya sido ingresado
            if not cuenta_input.strip():
                st.warning("⚠️ El campo Cuenta es obligatorio.")
                return

            # Verificar que al menos un campo adicional haya sido ingresado
            campos_adicionales = [
                ano_input,
                cuota_input,
                transacciones_input,
                tasa_input,
                comprob_input,
                capital_input,
                # sistema_input,
            ]

            if not ui_components.validar_campos_requeridos(campos_adicionales):
                st.warning(
                    "⚠️ Además de la cuenta, debés ingresar al menos un criterio adicional de búsqueda."
                )
                return

            # Construir condiciones WHERE dinámicamente
            conditions = []
            # No necesitamos base_condition ya que usamos INNER JOIN en la consulta SQL

            # # IMPORTANTE: Poner el filtro de sistema PRIMERO para optimizar la consulta
            # if sistema_input.strip():
            #     sistemas = [
            #         x.strip() for x in sistema_input.split(",") if x.strip().isdigit()
            #     ]
            #     if sistemas:
            #         sistemas_str = ",".join(sistemas)
            #         conditions.append(f"t.c_sistema = {sistemas_str}")

            # Procesar cada campo
            if cuenta_input.strip():
                cuentas = [x.strip() for x in cuenta_input.split(',') if x.strip().isdigit()]
                if cuentas:
                    cuentas_str = ','.join(cuentas)
                    conditions.append(f"t.c_cuenta = {cuentas_str}")

            if ano_input.strip():
                anos = [x.strip() for x in ano_input.split(',') if x.strip().isdigit()]
                if anos:
                    anos_str = ','.join(anos)
                    conditions.append(f"n_ano IN ({anos_str})")

            if cuota_input.strip():
                cuotas = [x.strip() for x in cuota_input.split(',') if x.strip().isdigit()]
                if cuotas:
                    cuotas_str = ','.join(cuotas)
                    conditions.append(f"n_cuota IN ({cuotas_str})")

            if transacciones_input.strip():
                transacs = [x.strip() for x in transacciones_input.split(',') if x.strip().isdigit()]
                if transacs:
                    transacs_str = ','.join(transacs)
                    conditions.append(f"t.n_transac IN ({transacs_str})")

            if tasa_input.strip():
                tasas = [x.strip() for x in tasa_input.split(',') if x.strip().isdigit()]
                if tasas:
                    tasas_str = ','.join(tasas)
                    conditions.append(f"c_tasa IN ({tasas_str})")

            if comprob_input.strip():
                comprobs = [x.strip() for x in comprob_input.split(',') if x.strip().isdigit()]
                if comprobs:
                    comprobs_str = ','.join(comprobs)
                    conditions.append(f"n_comprob IN ({comprobs_str})")

            if capital_input.strip():
                def es_numero_valido(s):
                    try:
                        float(s)
                        return True
                    except ValueError:
                        return False

                capitals = [x.strip() for x in capital_input.split(",") if es_numero_valido(x.strip())]
                if capitals:
                    if len(capitals) == 1:
                        conditions.append(f"i_capital = {capitals[0]}")
                    else:
                        capitals_str = ",".join(capitals)
                        conditions.append(f"i_capital ={capitals_str}")

            # Mostrar criterios de búsqueda
            criterios = []
            # if sistema_input.strip():
            #     criterios.append(f"🎯 Sistema: {sistema_input.strip()}")
            if cuenta_input.strip():
                criterios.append(f"Cuenta: {cuenta_input.strip()}")
            if ano_input.strip():
                criterios.append(f"Año: {ano_input.strip()}")
            if cuota_input.strip():
                criterios.append(f"Cuota: {cuota_input.strip()}")
            if transacciones_input.strip():
                trans_texto = transacciones_input.strip()[:50]
                if len(transacciones_input.strip()) > 50:
                    trans_texto += "..."
                criterios.append(f"Transacciones: {trans_texto}")
            if tasa_input.strip():
                criterios.append(f"Tasa: {tasa_input.strip()}")
            if comprob_input.strip():
                comp_texto = comprob_input.strip()[:50]
                if len(comprob_input.strip()) > 50:
                    comp_texto += "..."
                criterios.append(f"Comprobantes: {comp_texto}")
            if capital_input.strip():
                criterios.append(f"Capital: {capital_input.strip()}")

            mensaje_criterios = "🔍 Consultando cuenta corriente con criterios"
            # if sistema_input.strip():
            #     mensaje_criterios = f"🔍 Consultando cuenta corriente (Sistema {sistema_input.strip()}) con criterios"

            ui_components.mostrar_criterios_busqueda(criterios, mensaje_criterios)

            # Crear controles de búsqueda
            spinner_container, cancel_container, cancel_key = ui_components.crear_controles_busqueda("ctacte")

            # Mostrar botón de cancelar
            ui_components.mostrar_boton_cancelar(cancel_container, "ctacte")

            # Construir query completa
            all_conditions = conditions

            # Ejecutar consulta
            def consulta_ctacte():
                return db_manager.consultar_cuenta_corriente(all_conditions)

            df = ui_components.ejecutar_con_spinner(
                spinner_container,
                "💳 Consultando cuenta corriente... Presioná 'Cancelar Búsqueda' si querés detener.",
                consulta_ctacte
            )

            # Limpiar controles
            ui_components.limpiar_controles(spinner_container, cancel_container, cancel_key)

            if df is not None:
                # Mostrar estadísticas básicas
                columnas_metricas = {
                    "total": "Total registros",
                    "cuenta": "Cuentas únicas",
                    "transaccion": "Transacciones únicas",
                    "tasa": "Tasas únicas",
                    "sistema": "Sistemas únicos",
                }
                ui_components.mostrar_estadisticas_basicas(df, columnas_metricas)

                # Mostrar resultados
                ui_components.mostrar_resultados(df, "ctacte_consulta")

        except Exception as e:
            st.error(self.messages["errors"]["database_error"].format(error=e))


# Instancia global de consulta de cuenta corriente
consulta_cuenta_corriente = ConsultaCuentaCorriente()
