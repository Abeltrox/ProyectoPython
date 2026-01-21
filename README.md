# Sistema de Gestión de Herramientas Comunitarias

Sistema completo para administrar el préstamo de herramientas entre vecinos de una comunidad.

## 📋 Características

### Gestión de Herramientas
- Registro de herramientas con información detallada
- Control de stock en tiempo real
- Estados: activa, en reparación, fuera de servicio
- Categorización por tipo (construcción, jardinería, etc.)

### Gestión de Usuarios
- Dos tipos de usuario: residente y administrador
- Autenticación con contraseñas hasheadas
- Registro completo de datos de contacto

### Gestión de Préstamos
- Sistema de solicitudes para usuarios
- Aprobación de préstamos por administradores
- Control automático de disponibilidad
- Registro de devoluciones
- Alertas de préstamos vencidos

### Consultas e Informes
- Herramientas con stock bajo
- Préstamos activos y vencidos
- Historial por usuario
- Ranking de herramientas más solicitadas
- Usuarios más activos

### Registro de Eventos
- Log completo de todas las operaciones
- Filtrado por nivel (INFO, WARNING, ERROR)
- Trazabilidad de errores

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- No requiere librerías externas (usa solo módulos estándar)

### Estructura del Proyecto

```
proyecto/
│
├── main.py                          # Programa principal
├── README.md                        # Este archivo
│
├── modulos/                         # Módulos del sistema
│   ├── __init__.py
│   ├── gestion_herramientas.py
│   ├── gestion_usuarios.py
│   ├── gestion_prestamos.py
│   ├── autenticacion.py
│   ├── consultas.py
│   └── logger.py
│
├── datos/                           # Archivos de persistencia (generados automáticamente)
│   ├── herramientas.json
│   ├── usuarios.json
│   ├── prestamos.json
│   └── solicitudes.json
│
├── logs/                            # Registro de eventos (generado automáticamente)
│   └── sistema.log
│
└── pruebas/                         # Casos de prueba
    ├── test_herramientas.py
    ├── test_usuarios.py
    ├── test_prestamos.py
    └── datos_prueba.md
```

## 📝 Ejecución

### Iniciar el Sistema

```bash
python main.py
```

### Primer Inicio

El sistema crea automáticamente un usuario administrador por defecto:

- **ID:** admin
- **Contraseña:** admin123

⚠️ **IMPORTANTE:** Cambie esta contraseña después del primer inicio.

## 👥 Tipos de Usuario

### Administrador
Puede realizar todas las operaciones:
- Gestionar herramientas (crear, editar, eliminar)
- Gestionar usuarios (registrar vecinos)
- Aprobar o rechazar solicitudes de préstamo
- Registrar préstamos directamente
- Registrar devoluciones
- Ver todos los informes y estadísticas

### Usuario/Residente
Tiene acceso limitado a:
- Consultar herramientas disponibles
- Ver cuándo estará disponible una herramienta prestada
- Crear solicitudes de préstamo
- Ver sus propios préstamos activos

## 📊 Flujo de Trabajo

### Para Usuarios

1. **Consultar herramientas disponibles**
   - Ver qué herramientas están disponibles
   - Conocer el stock actual

2. **Solicitar préstamo**
   - Seleccionar herramienta
   - Indicar cantidad y días necesarios
   - Agregar observaciones

3. **Esperar aprobación**
   - El administrador revisa la solicitud
   - Puede aprobarla o rechazarla

4. **Recibir la herramienta**
   - Una vez aprobada, se genera el préstamo
   - El stock se ajusta automáticamente

5. **Devolver la herramienta**
   - El administrador registra la devolución
   - El stock se restaura

### Para Administradores

1. **Registrar herramientas nuevas**
   - Ingresar datos completos
   - Establecer cantidad inicial

2. **Registrar vecinos**
   - Crear perfiles de usuario
   - Asignar credenciales de acceso

3. **Revisar solicitudes**
   - Ver solicitudes pendientes
   - Aprobar o rechazar con justificación

4. **Registrar préstamos directos**
   - Opción para préstamos sin solicitud previa
   - Útil para casos especiales

5. **Registrar devoluciones**
   - Marcar préstamos como devueltos
   - Agregar observaciones sobre el estado

6. **Monitorear el sistema**
   - Revisar préstamos vencidos
   - Verificar stock bajo
   - Analizar estadísticas de uso

## 🔒 Seguridad

- Las contraseñas se almacenan hasheadas (SHA-256)
- Sistema de autenticación robusto
- Separación clara de permisos por tipo de usuario
- Registro de todos los intentos de acceso

## 📁 Persistencia de Datos

Todos los datos se almacenan en formato JSON:

- **herramientas.json:** Catálogo de herramientas
- **usuarios.json:** Registro de vecinos
- **prestamos.json:** Historial de préstamos
- **solicitudes.json:** Solicitudes pendientes y procesadas

## 📈 Informes Disponibles

1. **Stock Bajo:** Herramientas que necesitan reposición
2. **Préstamos Activos:** Herramientas actualmente prestadas
3. **Préstamos Vencidos:** Devoluciones atrasadas
4. **Historial de Usuario:** Todos los préstamos de un vecino
5. **Herramientas Populares:** Las más solicitadas
6. **Usuarios Activos:** Vecinos más participativos

## 🐛 Registro de Errores

El sistema registra automáticamente:

- Inicios de sesión exitosos y fallidos
- Operaciones CRUD en todas las entidades
- Errores de validación
- Intentos de préstamo sin stock
- Cualquier excepción del sistema

Ubicación del log: `logs/sistema.log`

## 🧪 Pruebas

El directorio `pruebas/` contiene:

- Scripts de prueba automatizados
- Casos de entrada y salida esperada
- Datos de ejemplo para testing

Para ejecutar las pruebas:

```bash
python -m pytest pruebas/
```

## 💡 Casos de Uso Comunes

### Caso 1: Nuevo Vecino
```
1. Admin → Gestión de Usuarios → Crear Usuario
2. Usuario recibe ID y contraseña
3. Usuario inicia sesión y cambia contraseña
```

### Caso 2: Solicitar Taladro
```
1. Usuario → Consultar Herramientas
2. Usuario → Solicitar Préstamo (ID del taladro)
3. Admin → Aprobar Solicitudes
4. Sistema ajusta stock automáticamente
```

### Caso 3: Devolución
```
1. Admin → Gestión de Préstamos → Registrar Devolución
2. Ingresar ID del préstamo
3. Agregar observaciones sobre el estado
4. Sistema restaura stock automáticamente
```

### Caso 4: Herramienta No Disponible
```
1. Usuario consulta herramientas
2. Sistema muestra fecha de próxima devolución
3. Usuario puede solicitar para después de esa fecha
```

## 🔧 Solución de Problemas

### Error: No se puede guardar datos
- Verificar permisos de escritura en carpetas `datos/` y `logs/`
- Asegurar que no hay otro proceso usando los archivos

### Error: No puedo iniciar sesión
- Verificar ID de usuario (case-sensitive)
- Usuario administrador por defecto: admin / admin123
- Revisar logs para ver intentos fallidos

### Error: Préstamo rechazado
- Verificar stock disponible
- Confirmar que la herramienta está en estado "activa"
- Revisar que la cantidad solicitada no excede el disponible

## 📞 Soporte

Para reportar problemas o sugerir mejoras:

1. Revisar el archivo de logs: `logs/sistema.log`
2. Verificar la documentación en este README
3. Contactar al administrador del sistema

## 📄 Licencia

Este proyecto es de código abierto para uso comunitario.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Mantener el estilo de código consistente
2. Documentar nuevas funcionalidades
3. Agregar pruebas para nuevas características
4. Actualizar el README según sea necesario

---

**Versión:** 1.0.0  
**Última actualización:** Enero 2026  
**Desarrollado para:** Comunidades y conjuntos residenciales