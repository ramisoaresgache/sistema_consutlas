"""
Módulo de consulta de lotes bancarios
Maneja toda la lógica de la pestaña de lotes bancarios
"""

import streamlit as st
from database import db_manager
from ui_components import ui_components
from config import TABS_CONFIG, MESSAGES


class ConsultaLotesBancarios:
    """Manejador de consultas de lotes bancarios"""
    
    def __init__(self):
        self.config = TABS_CONFIG["lotes"]
        self.messages = MESSAGES
    
    def mostrar_interfaz(self):
        """Muestra la interfaz de consulta de lotes bancarios"""
        st.header(self.config["header"])
        st.write(self.config["description"])

        # Crear formulario con múltiples campos
        with st.form("consulta_banco_form"):
            col1, col2 = st.columns(2)

            with col1:
                # Campo para cuentas
                cuentas_input = st.text_input(
                    "Cuenta/s (podes poner mas de 1 es opcional):", 
                    placeholder="Ej: 60194, 60195, 60196",
                    help="Ingresá los números de cuenta separados por coma"
                )

                # Campo para registros
                registros_input = st.text_input(
                    "Importe (solo podes poner 1 importe):", 
                    placeholder="Ej: 10575",
                    help="Ingresá los números de registro separados por coma"
                )

            with col2:
                # Campo para fecha de cobro
                fecha_cobro = st.date_input(
                    "Fecha de cobro (solo 1 fecha podes poner):",
                    value=None,
                    help="Seleccioná una fecha del calendario"
                )

                # Campo para comprobantes
                comprobantes_input_banco = st.text_input(
                    "Comprobante/s (podes poner mas de 1 es opcional):", 
                    placeholder="Ej: 10802142352,10802142913",
                    help="Ingresá los números de comprobante separados por coma"
                )

            # Botón de búsqueda
            submitted = st.form_submit_button("🔍 Buscar en Banco", use_container_width=True)

        if submitted:
            self.procesar_busqueda(cuentas_input, registros_input, fecha_cobro, comprobantes_input_banco)
    
    def procesar_busqueda(self, cuentas_input, registros_input, fecha_cobro, comprobantes_input_banco):
        """Procesa la búsqueda de lotes bancarios"""
        try:
            # Construir condiciones WHERE dinámicamente
            conditions = []

            # Procesar cuentas
            if cuentas_input.strip():
                cuentas = [x.strip() for x in cuentas_input.split(',') if x.strip().isdigit()]
                if cuentas:
                    cuentas_str = ','.join(cuentas)
                    conditions.append(f"c_cuenta IN ({cuentas_str})")

            # Procesar fecha de cobro
            if fecha_cobro:
                fecha_str = fecha_cobro.strftime("%d/%m/%Y")
                conditions.append(f"f_cobro = '{fecha_str}'")

            # Procesar registros
            if registros_input.strip():
                registros = [x.strip() for x in registros_input.split(',') if x.strip().isdigit()]
                if registros:
                    registros_str = ','.join(registros)
                    conditions.append(f"i_registro = {registros_str}")

            # Procesar comprobantes
            if comprobantes_input_banco.strip():
                comprobantes = [x.strip() for x in comprobantes_input_banco.split(',') if x.strip().isdigit()]
                if comprobantes:
                    comprobantes_str = ','.join(comprobantes)
                    conditions.append(f"n_comprob IN ({comprobantes_str})")

            # Verificar que al menos una condición esté presente
            if not conditions:
                st.warning(self.messages["validation"]["min_one_field"])
                return
            
            # Mostrar criterios de búsqueda
            criterios = []
            if cuentas_input.strip():
                criterios.append(f"Cuentas: {cuentas_input.strip()}")
            if fecha_cobro:
                criterios.append(f"Fecha: {fecha_cobro.strftime('%d/%m/%Y')}")
            if registros_input.strip():
                criterios.append(f"Importe: {registros_input.strip()}")
            if comprobantes_input_banco.strip():
                comp_texto = comprobantes_input_banco.strip()[:50]
                if len(comprobantes_input_banco.strip()) > 50:
                    comp_texto += "..."
                criterios.append(f"Comprobantes: {comp_texto}")
            
            ui_components.mostrar_criterios_busqueda(criterios, "🔍 Buscando en lotes bancarios con criterios")
            
            # Crear controles de búsqueda
            spinner_container, cancel_container, cancel_key = ui_components.crear_controles_busqueda("banco")
            
            # Mostrar botón de cancelar
            ui_components.mostrar_boton_cancelar(cancel_container, "banco")
            
            # Ejecutar consulta
            def consulta_lotes():
                return db_manager.consultar_lotes_bancarios(conditions)
            
            df = ui_components.ejecutar_con_spinner(
                spinner_container,
                "🏦 Consultando lotes bancarios... Presioná 'Cancelar Búsqueda' si querés detener.",
                consulta_lotes
            )
            
            # Limpiar controles
            ui_components.limpiar_controles(spinner_container, cancel_container, cancel_key)
            
            if df is not None:
                # Mostrar estadísticas básicas
                columnas_metricas = {
                    "total": "Total registros",
                    "cuenta": "Cuentas únicas",
                    "fecha_cobro": "Fechas únicas"
                }
                ui_components.mostrar_estadisticas_basicas(df, columnas_metricas)
                
                # Mostrar resultados
                ui_components.mostrar_resultados(df, "bco_cab_consulta")
            
        except Exception as e:
            st.error(self.messages["errors"]["database_error"].format(error=e))


# Instancia global de consulta de lotes bancarios
consulta_lotes_bancarios = ConsultaLotesBancarios()
