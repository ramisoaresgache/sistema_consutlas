"""
Módulo de autenticación y gestión de sesiones
Maneja login, logout y sesiones persistentes
"""

import streamlit as st
from database import db_manager
from usuarios_autorizados import esta_autorizado, CONFIGURACION_ACCESO
from config import MESSAGES


class AuthManager:
    """Manejador de autenticación y sesiones"""

    def __init__(self):
        self.messages = MESSAGES
        # Detectar si Streamlit tiene la nueva API de query_params
        self._has_new_query_params = hasattr(st, "query_params")

    def _get_query_params(self):
        """Obtiene los query parameters usando la API correcta según la versión de Streamlit"""
        if self._has_new_query_params:
            try:
                return dict(st.query_params)
            except Exception:
                # Si falla, usar API anterior como fallback
                return st.experimental_get_query_params()
        else:
            return st.experimental_get_query_params()

    def _set_query_params(self, **params):
        """Establece los query parameters usando la API correcta según la versión de Streamlit"""
        if self._has_new_query_params:
            try:
                for key, value in params.items():
                    st.query_params[key] = value
            except Exception:
                # Si falla, usar API anterior como fallback
                st.experimental_set_query_params(**params)
        else:
            st.experimental_set_query_params(**params)

    def _clear_query_params(self):
        """Limpia los query parameters usando la API correcta según la versión de Streamlit"""
        if self._has_new_query_params:
            try:
                st.query_params.clear()
            except Exception:
                # Si falla, usar API anterior como fallback
                st.experimental_set_query_params()
        else:
            st.experimental_set_query_params()

    def verificar_login(self, legajo, password):
        """Verifica las credenciales del usuario contra la base de datos y autorización"""
        try:
            # Convertir legajo a entero para la consulta
            legajo_int = int(legajo)
            password_int = int(password)

            # PASO 1: Verificar si el usuario está autorizado
            if not esta_autorizado(legajo):
                # Usuario no autorizado
                mensaje_error = CONFIGURACION_ACCESO["mensaje_acceso_denegado"]
                if CONFIGURACION_ACCESO["mostrar_legajo_en_error"]:
                    mensaje_error += f" (Legajo: {legajo})"
                return "no_autorizado", mensaje_error

            # PASO 2: Si está autorizado, verificar credenciales en la base
            login_exitoso, nombre = db_manager.verificar_usuario_login(legajo_int, password_int)

            if login_exitoso:
                return "exito", nombre
            return "credenciales_incorrectas", None

        except ValueError:
            # Error si legajo o password no son números
            return "credenciales_incorrectas", None
        except Exception as e:
            st.error(f"Error al verificar credenciales: {e}")
            return "error", None

    def mostrar_login(self):
        """Muestra la pantalla de login"""
        # Centrar el título usando HTML y CSS
        st.markdown(
            f"""
            <div style='text-align: center;'>
                <h1>{self.messages["login"]["title"]}</h1>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.subheader(self.messages["login"]["subtitle"])

            with st.form("login_form"):
                legajo = st.text_input(
                    "Legajo:",
                    placeholder="Ingresá tu número de legajo",
                    help=self.messages["login"]["legajo_help"],
                )

                password = st.text_input(
                    "Contraseña:",
                    type="password",
                    placeholder="Ingresá tu contraseña",
                    help=self.messages["login"]["password_help"],
                )

                login_button = st.form_submit_button(
                    self.messages["login"]["button_text"], 
                    use_container_width=True
                )

                if login_button:
                    if not legajo or not password:
                        st.error(self.messages["login"]["fields_required"])
                    else:
                        with st.spinner("Verificando credenciales..."):
                            resultado, data = self.verificar_login(legajo, password)

                        if resultado == "exito":
                            st.session_state.logged_in = True
                            st.session_state.user_legajo = legajo
                            st.session_state.user_nombre = data

                            # Crear sesión persistente
                            self.crear_sesion_persistente(legajo)

                            st.success(self.messages["login"]["welcome"].format(nombre=data))
                            st.rerun()
                        elif resultado == "no_autorizado":
                            st.error(data)  # data contiene el mensaje de error personalizado
                        elif resultado == "credenciales_incorrectas":
                            st.error(self.messages["login"]["credentials_error"])
                        else:
                            st.error(self.messages["login"]["unexpected_error"])

    def cerrar_sesion(self):
        """Cierra la sesión del usuario"""
        # Limpiar session_state
        for key in ["logged_in", "user_legajo", "user_nombre", "session_token"]:
            if key in st.session_state:
                del st.session_state[key]

        # Limpiar query params usando el método auxiliar
        self._clear_query_params()
        st.rerun()

    def verificar_sesion_persistente(self):
        """Verifica si hay una sesión persistente válida"""
        query_params = self._get_query_params()

        if "session_token" in query_params and "user_legajo" in query_params:
            # Verificar que el token coincida con el legajo
            # Manejar tanto el formato nuevo (string) como el anterior (lista)
            if isinstance(query_params["session_token"], list):
                session_token = query_params["session_token"][0]
                user_legajo = query_params["user_legajo"][0]
            else:
                session_token = query_params["session_token"]
                user_legajo = query_params["user_legajo"]

            # Token simple: legajo codificado
            expected_token = f"token_{user_legajo}_{len(user_legajo)}"

            if session_token == expected_token:
                # Verificar que el usuario siga autorizado
                if not esta_autorizado(user_legajo):
                    # Usuario ya no autorizado, limpiar sesión
                    self._clear_query_params()
                    st.error("🚫 Tu autorización ha sido revocada. Contactá al administrador.")
                    return False

                # Restaurar sesión
                st.session_state.logged_in = True
                st.session_state.user_legajo = user_legajo
                st.session_state.session_token = session_token

                # Obtener nombre del usuario de la base de datos
                nombre = db_manager.obtener_nombre_usuario(int(user_legajo))
                if nombre:
                    st.session_state.user_nombre = nombre
                    return True

        return False

    def crear_sesion_persistente(self, legajo):
        """Crea una sesión persistente usando query parameters"""
        # Crear token simple
        session_token = f"token_{legajo}_{len(legajo)}"

        # Guardar en session_state
        st.session_state.session_token = session_token

        # Actualizar URL con parámetros usando el método auxiliar
        self._set_query_params(session_token=session_token, user_legajo=legajo)

    def inicializar_sesion(self):
        """Inicializa el estado de sesión"""
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        # Verificar sesión persistente antes de mostrar login
        if not st.session_state.logged_in:
            # Intentar restaurar sesión persistente
            if self.verificar_sesion_persistente():
                st.success(self.messages["session"]["restored"])
                st.rerun()

        # Verificar si el usuario está logueado
        if not st.session_state.logged_in:
            self.mostrar_login()
            st.stop()

    def esta_logueado(self):
        """Verifica si el usuario está logueado"""
        return st.session_state.get("logged_in", False)


# Instancia global del manejador de autenticación
auth_manager = AuthManager()
