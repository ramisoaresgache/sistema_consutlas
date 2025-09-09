# 🔍 Sistema de Consultas - Municipalidad de Vicente López

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Status](https://img.shields.io/badge/Status-Activo-green.svg)

Sistema web modularizado para consultas de base de datos municipales con autenticación segura y interfaz intuitiva.

## 📋 Descripción

El Sistema de Consultas es una aplicación web desarrollada en Python con Streamlit que permite a usuarios autorizados realizar consultas específicas sobre la base de datos municipal de recaudaciones. La aplicación incluye módulos especializados para diferentes tipos de consultas y un sistema robusto de autenticación.

## ✨ Características Principales

- 🔐 **Autenticación Segura**: Sistema de login con verificación de usuarios autorizados
- 📊 **Múltiples Módulos de Consulta**: 5 tipos especializados de búsquedas
- 💾 **Exportación a Excel**: Descarga de resultados en formato .xlsx
- 🔄 **Sesiones Persistentes**: Mantiene la sesión activa entre recargas
- 📱 **Interfaz Responsiva**: Adaptada para diferentes tamaños de pantalla
- ⚡ **Consultas Optimizadas**: Búsquedas rápidas con validaciones robustas
- 🛡️ **Manejo de Errores**: Sistema robusto de validación y error handling

## 🗂️ Módulos de Consulta

### 1. 📄 Consulta de Recibos
- Búsqueda por número/s de comprobante
- Validación de longitud (máximo 16 dígitos)
- Múltiples comprobantes separados por coma

### 2. 🏦 Consulta de Comprobantes
- Búsqueda por cuenta/s, fecha de cobro, importes y comprobantes
- Filtros flexibles y combinables
- Validación de formatos de fecha

### 3. 💳 Consulta de Cuenta Corriente
- Búsqueda por cuenta (obligatorio) + filtros adicionales
- Filtros: año, cuota, transacciones, tasa, comprobantes, capital
- Validaciones de tipos de datos

### 4. 📋 Declaraciones Juradas
- Búsqueda por CUIT, cuenta e ID simplificado
- Doble consulta: cabecera + régimen simplificado
- Validación de formato CUIT

### 5. 📅 Planes de Pago
- Búsqueda por número de plan (obligatorio) + cuota opcional
- Doble resultado: detalles del plan + transacciones
- Validaciones numéricas

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje principal
- **Streamlit**: Framework web
- **pandas**: Manipulación de datos
- **pyodbc**: Conexión a base de datos
- **openpyxl**: Exportación a Excel
- **python-dotenv**: Manejo de variables de entorno

## 📦 Instalación

### Prerrequisitos

1. **Python 3.11 o superior**
2. **Driver ODBC para Informix**: IBM INFORMIX ODBC DRIVER (64-bit)
3. **Acceso a la red municipal** (para conexión a base de datos)

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/ramisoaresgache/sistema_consutlas.git
   cd sistema_consutlas
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # En Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install streamlit pandas pyodbc openpyxl python-dotenv
   ```

4. **Configurar variables de entorno**:
   - Copiar `.env.example` a `.env`
   - Configurar los parámetros de base de datos:
   ```properties
   DB_DRIVER=IBM INFORMIX ODBC DRIVER (64-bit)
   DB_HOST=192.9.200.5
   DB_SERVICE=1521
   DB_DATABASE=recaudaciones
   DB_SERVER=munivl_tcp
   DB_PROTOCOL=onsoctcp
   DB_UID=tu_usuario
   DB_PWD=tu_contraseña
   ```

5. **Configurar usuarios autorizados**:
   - Editar `usuarios_autorizados.py`
   - Agregar legajos autorizados a la lista `USUARIOS_AUTORIZADOS`

## 🚀 Uso

### Ejecutar la aplicación:
```bash
streamlit run main.py
```

### Acceso:
1. Abrir navegador en `http://localhost:8501`
2. Ingresar legajo y contraseña
3. Seleccionar el módulo de consulta deseado
4. Realizar búsquedas y descargar resultados

## 📁 Estructura del Proyecto

```
sistema_consultas/
├── 📄 main.py                    # Archivo principal de la aplicación
├── 🔐 auth.py                    # Sistema de autenticación
├── ⚙️ config.py                  # Configuraciones centralizadas
├── 🗄️ database.py               # Manejo de conexión a BD
├── 🎨 ui_components.py           # Componentes de interfaz reutilizables
├── 👥 usuarios_autorizados.py    # Lista de usuarios permitidos
├── 📊 consultas/                 # Módulos de consulta especializados
│   ├── 📄 recibos.py            
│   ├── 🏦 lotes_bancarios.py    
│   ├── 💳 cuenta_corriente.py   
│   ├── 📋 declaraciones_juradas.py
│   └── 📅 planes.py             
├── 🔧 .env                       # Variables de entorno (configurar)
├── 📚 README.md                  # Este archivo
└── 📋 requirements.txt           # Dependencias Python
```

## 🔧 Configuración Detallada

### Base de Datos
El sistema se conecta a una base de datos Informix usando ODBC. La configuración se realiza en el archivo `.env`:

- **DB_DRIVER**: Driver ODBC de Informix
- **DB_HOST**: IP del servidor de base de datos
- **DB_SERVICE**: Puerto de conexión
- **DB_DATABASE**: Nombre de la base de datos
- **DB_SERVER**: Nombre del servidor Informix
- **DB_PROTOCOL**: Protocolo de conexión
- **DB_UID/DB_PWD**: Credenciales de acceso

### Usuarios Autorizados
Los usuarios se configuran en `usuarios_autorizados.py`:

```python
USUARIOS_AUTORIZADOS = [
    12345,  # Legajo del usuario 1
    67890,  # Legajo del usuario 2
    # Agregar más legajos según necesidad
]
```

### Personalización de Interfaz
Las configuraciones de UI se modifican en `config.py`:

- Títulos y mensajes
- Configuración de pestañas
- Mensajes de error y validación
- Configuración de página Streamlit

## 🔍 Funcionalidades Técnicas

### Sistema de Autenticación
- Verificación de credenciales contra base de datos
- Lista de usuarios autorizados configurable
- Sesiones persistentes con tokens seguros
- Logout automático por seguridad

### Manejo de Datos
- Consultas SQL optimizadas y seguras
- Validación de entrada para prevenir SQL injection
- Formateo automático de datos numéricos
- Manejo robusto de errores de conexión

### Interfaz de Usuario
- Componentes reutilizables y modulares
- Validaciones en tiempo real
- Métricas automáticas de resultados
- Exportación a Excel con un clic
- Resultados persistentes entre búsquedas

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error de conexión a base de datos**:
   - Verificar configuración en `.env`
   - Comprobar conectividad de red
   - Validar credenciales de acceso

2. **Usuario no autorizado**:
   - Verificar que el legajo esté en `usuarios_autorizados.py`
   - Comprobar que las credenciales sean correctas

3. **Error al exportar Excel**:
   - Verificar que `openpyxl` esté instalado
   - Comprobar permisos de escritura en directorio

4. **Aplicación lenta**:
   - Revisar consultas SQL en `database.py`
   - Optimizar filtros de búsqueda
   - Verificar performance de red

## 📊 Logs y Debugging

El sistema incluye logging detallado para debugging:
- Errores de conexión a BD
- Validaciones fallidas
- Problemas de autenticación
- Errores de exportación

## 🔒 Seguridad

- **Autenticación**: Doble verificación (BD + lista autorizada)
- **Sesiones**: Tokens seguros con validación
- **SQL Injection**: Consultas parametrizadas
- **Validaciones**: Input validation en todos los campos
- **Logs**: Registro de accesos y errores

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es propiedad de la **Municipalidad de Vicente López** y está destinado exclusivamente para uso interno municipal.

## 👨‍💻 Autor

**Rami Soares Gache**  
Municipalidad de Vicente López  
Sistema de Recaudaciones

---

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema:

- **Email**: sistemas@vicentelopez.gov.ar
- **Interno**: Extensión XXXX
- **Ubicación**: Oficina de Sistemas - Edificio Municipal

---

*Última actualización: Julio 2025*
*Versión: 2.0.0*
