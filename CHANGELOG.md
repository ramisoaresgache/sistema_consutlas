# 📝 Changelog - Sistema de Consultas

Todas las mejoras notables del proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [2.0.0] - 2025-07-27

### 🎉 Agregado
- **Sistema de autenticación robusto** con doble validación
- **5 módulos especializados** de consulta (recibos, lotes bancarios, cuenta corriente, declaraciones juradas, planes)
- **Exportación a Excel** con un clic
- **Sesiones persistentes** que mantienen login entre recargas
- **Interfaz responsive** adaptada a diferentes pantallas
- **Validaciones exhaustivas** en todos los formularios
- **Métricas automáticas** de resultados
- **Sistema de debugging** completo
- **Documentación técnica** detallada

### 🛠️ Mejorado
- **Performance de consultas** optimizada
- **Manejo de errores** más robusto
- **Interfaz de usuario** más intuitiva
- **Código modularizado** y reutilizable
- **Seguridad** con consultas parametrizadas

### 🐛 Corregido
- **Error "Bad message format"** por exceso de métricas
- **Duplicación de resultados** en todas las consultas
- **Funciones deprecadas** de Streamlit actualizadas
- **Validaciones de DataFrame** mejoradas
- **Limpieza de session_state** optimizada

### 🔧 Técnico
- Migración a Streamlit 1.28+
- Compatibilidad con `st.query_params` y fallback a API anterior
- Límite de 4 métricas para evitar errores de índice
- Lógica condicional para resultados persistentes vs nuevos
- Validaciones robustas en todas las capas

## [1.0.0] - 2025-01-01

### 🎉 Lanzamiento Inicial
- Sistema básico de consultas
- Conexión a base de datos Informix
- Interfaz web con Streamlit
- Autenticación básica

---

## 🏷️ Tipos de Cambios

- **Agregado**: para nuevas funcionalidades
- **Mejorado**: para cambios en funcionalidades existentes
- **Deprecado**: para funcionalidades que serán removidas
- **Removido**: para funcionalidades removidas
- **Corregido**: para corrección de bugs
- **Seguridad**: para vulnerabilidades corregidas
- **Técnico**: para cambios internos sin impacto en funcionalidad

---

## 📅 Próximas Versiones

### [2.1.0] - Planificado
- [ ] Dashboard con métricas generales
- [ ] Filtros avanzados por fecha
- [ ] bot chat con IA para consultas sobre sistema
- [ ] Notificaciones en tiempo real
- [ ] Gráficos interactivos

### [2.2.0] - Planificado
- [ ] API REST para integraciones
- [ ] Programación de consultas automáticas
- [ ] Alertas por email
- [ ] Auditoria de accesos
- [ ] Modo oscuro en la interfaz

---

*Para sugerir nuevas funcionalidades o reportar bugs, contactar al equipo de desarrollo.*
