# Sistema de Consultas con Autenticación

## 🔐 Sistema de Login

Este sistema ahora incluye autenticación de usuarios basada en la tabla `usuarios` de la base de datos.

### Credenciales de Acceso
- **Usuario**: Número de legajo (n_legajo)
- **Contraseña**: Mismo número de legajo (temporal)

### 👥 Gestión de Usuarios

#### Tabla de Usuarios
La tabla `usuarios` debe tener la siguiente estructura:
```sql
CREATE TABLE usuarios (
    n_legajo INTEGER PRIMARY KEY,
    d_nombre VARCHAR(100) NOT NULL,
    c_activo CHAR(1) DEFAULT 'S',
    f_alta DATE DEFAULT TODAY,
    c_rol VARCHAR(20) DEFAULT 'consultor_basico'
);
```

#### Crear Usuarios de Prueba
Para crear usuarios de prueba, ejecutá:
```bash
python crear_usuarios.py
```

### 🛡️ Sistema de Permisos

#### Roles Disponibles
1. **Administrador**: Acceso completo al sistema
2. **Consultor Senior**: Acceso a todas las consultas y estadísticas
3. **Consultor Básico**: Acceso básico a consultas principales
4. **Solo Lectura**: Solo puede ver la tabla de recibos

#### Configuración de Permisos
Los permisos se configuran en `config_usuarios.py`. Para agregar un usuario administrador:
```python
USUARIOS_ROLES = {
    '1234': 'administrador',  # Tu legajo aquí
    '5678': 'consultor_senior',
}
```

### 🚀 Funcionalidades del Login

#### Pantalla de Bienvenida
- Saludo personalizado con el nombre del usuario
- Mensaje motivacional: "Hola [Nombre], que tengas un lindo día!"

#### Sesión de Usuario
- Mantiene la sesión activa durante el uso
- Botón de "Cerrar Sesión" siempre visible
- Protección contra acceso no autorizado

### 📋 Próximas Mejoras

1. **Cambio de Contraseñas**: Permitir que usuarios cambien sus contraseñas
2. **Tabla de Permisos**: Mover permisos a la base de datos
3. **Auditoría**: Registro de accesos y acciones de usuarios
4. **Recuperación de Contraseña**: Sistema para resetear contraseñas
5. **Sesiones Temporales**: Expiración automática de sesiones

### 🔧 Archivos del Sistema

- `sistema_consultas.py`: Aplicación principal con login
- `permisos_usuario.py`: Gestión de permisos y roles
- `config_usuarios.py`: Configuración de roles y usuarios
- `crear_usuarios.py`: Script para crear usuarios de prueba

### 💡 Uso Recomendado

1. **Primera vez**: Ejecutá `crear_usuarios.py` para crear usuarios de prueba
2. **Configuración**: Editá `config_usuarios.py` para asignar roles
3. **Producción**: Agregá usuarios reales a la tabla `usuarios`
4. **Mantenimiento**: Usá el rol administrador para gestionar el sistema

### ⚠️ Seguridad

- Las contraseñas por defecto son iguales al legajo (temporal)
- Cambiá las contraseñas en producción
- El archivo `.env` sigue siendo crítico para la seguridad
- Los permisos se verifican en cada acción

---

**¡El sistema está listo para usar con autenticación completa!** 🎉
