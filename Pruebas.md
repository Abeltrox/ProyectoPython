# Datos de Prueba

## Casos de Prueba para el Sistema de Gestión de Herramientas

### 1. Pruebas de Herramientas

#### Caso 1.1: Crear Herramienta Válida
**Entrada:**
```
Nombre: Taladro Eléctrico
Categoría: construcción
Cantidad: 3
Estado: activa
Valor: 250000
```
**Salida Esperada:**
- ✓ Herramienta creada con ID H001
- Log: [INFO] Herramienta creada: Taladro Eléctrico (ID: H001)

#### Caso 1.2: Crear Herramienta con Datos Inválidos
**Entrada:**
```
Nombre: (vacío)
Categoría: construcción
Cantidad: -5
Estado: activa
Valor: 100000
```
**Salida Esperada:**
- ✗ Error: Nombre y categoría son obligatorios
- Log: [ERROR] Intento de crear herramienta con valores inválidos

#### Caso 1.3: Actualizar Herramienta
**Entrada:**
```
ID: H001
Cantidad: 5 (actualización)
```
**Salida Esperada:**
- ✓ Herramienta actualizada
- Stock actualizado de 3 a 5

#### Caso 1.4: Buscar Herramienta por Categoría
**Entrada:**
```
Campo: categoría
Valor: construcción
```
**Salida Esperada:**
- Lista de todas las herramientas de construcción

---

### 2. Pruebas de Usuarios

#### Caso 2.1: Crear Usuario Residente
**Entrada:**
```
Nombres: Juan Carlos
Apellidos: Pérez González
Teléfono: 3001234567
Dirección: Calle 123 #45-67
Tipo: residente
Password: mipassword123
```
**Salida Esperada:**
- ✓ Usuario creado con ID U001
- Log: [INFO] Usuario creado: Juan Carlos Pérez González

#### Caso 2.2: Crear Usuario con Tipo Inválido
**Entrada:**
```
Tipo: gerente (no válido)
```
**Salida Esperada:**
- ✗ Error: Tipo debe ser: residente, administrador

#### Caso 2.3: Autenticación Exitosa
**Entrada:**
```
ID: admin
Password: admin123
```
**Salida Esperada:**
- ✓ Bienvenido Administrador
- Log: [INFO] Usuario autenticado exitosamente

#### Caso 2.4: Autenticación Fallida
**Entrada:**
```
ID: admin
Password: wrongpassword
```
**Salida Esperada:**
- ✗ Usuario o contraseña incorrectos
- Log: [WARNING] Intento de acceso fallido para usuario: admin

---

### 3. Pruebas de Préstamos

#### Caso 3.1: Crear Solicitud de Préstamo
**Entrada:**
```
Usuario: U001
Herramienta: H001
Cantidad: 1
Días: 7
Observaciones: Necesito para reparación
```
**Salida Esperada:**
- ✓ Solicitud creada con ID S001
- Estado: pendiente

#### Caso 3.2: Aprobar Solicitud con Stock Suficiente
**Entrada:**
```
ID Solicitud: S001
Stock disponible: 3
```
**Salida Esperada:**
- ✓ Solicitud aprobada
- Préstamo creado con ID P001
- Stock ajustado: 3 → 2

#### Caso 3.3: Intentar Préstamo sin Stock
**Entrada:**
```
Usuario: U001
Herramienta: H001
Cantidad: 10 (excede stock)
```
**Salida Esperada:**
- ✗ Error: No hay suficiente stock disponible
- Log: [ERROR] Intento de préstamo sin stock suficiente

#### Caso 3.4: Registrar Devolución
**Entrada:**
```
ID Préstamo: P001
Observaciones: En buen estado
```
**Salida Esperada:**
- ✓ Devolución registrada
- Estado del préstamo: devuelto
- Stock restaurado: 2 → 3

#### Caso 3.5: Préstamo Vencido
**Entrada:**
```
Fecha inicio: 2026-01-01
Días: 7
Fecha actual: 2026-01-15
```
**Salida Esperada:**
- Préstamo aparece en lista de vencidos
- Diferencia: 7 días de retraso

---

### 4. Pruebas de Consultas

#### Caso 4.1: Stock Bajo
**Entrada:**
```
Límite: 3
Herramientas: H001 (2 unidades), H002 (5 unidades)
```
**Salida Esperada:**
- Lista: H001 únicamente

#### Caso 4.2: Herramientas Más Solicitadas
**Datos:**
```
H001: 10 préstamos
H002: 5 préstamos
H003: 15 préstamos
```
**Salida Esperada:**
```
1. H003 - 15 préstamos
2. H001 - 10 préstamos
3. H002 - 5 préstamos
```

#### Caso 4.3: Historial de Usuario
**Entrada:**
```
Usuario: U001
```
**Salida Esperada:**
- Lista completa de préstamos activos y devueltos
- Ordenados cronológicamente

---

### 5. Pruebas de Integración

#### Caso 5.1: Flujo Completo de Préstamo
**Secuencia:**
```
1. Usuario consulta herramientas disponibles
   → Ve H001 con 3 unidades
2. Usuario crea solicitud
   → Solicitud S001 pendiente
3. Admin aprueba solicitud
   → Préstamo P001 activo, stock: 2
4. Pasa el tiempo (7 días)
5. Admin registra devolución
   → Préstamo P001 devuelto, stock: 3
```
**Validaciones:**
- Stock se mantiene consistente
- Estados cambian correctamente
- Fechas se registran apropiadamente

#### Caso 5.2: Múltiples Préstamos Simultáneos
**Datos:**
```
H001 stock inicial: 5
- U001 solicita 2 → aprobado (stock: 3)
- U002 solicita 2 → aprobado (stock: 1)
- U003 solicita 2 → rechazado (stock insuficiente)
```
**Validaciones:**
- Primer préstamo exitoso
- Segundo préstamo exitoso
- Tercer préstamo rechazado apropiadamente

---

### 6. Pruebas de Seguridad

#### Caso 6.1: Password Hasheado
**Validación:**
```
Password ingresado: admin123
Almacenado: [hash SHA-256]
```
**Resultado:**
- Password nunca almacenado en texto plano
- Hash generado correctamente

#### Caso 6.2: Acceso por Permisos
**Usuario residente intenta:**
```
- Crear herramienta → BLOQUEADO
- Aprobar solicitud → BLOQUEADO
- Consultar herramientas → PERMITIDO
```

---

### 7. Pruebas de Logs

#### Caso 7.1: Eventos Registrados
**Operaciones:**
```
- Login exitoso
- Creación de herramienta
- Préstamo sin stock
- Error de sistema
```
**Validación:**
- Todas registradas en logs/sistema.log
- Formato correcto: [timestamp] [nivel] mensaje
- Niveles correctos (INFO, WARNING, ERROR)

#### Caso 7.2: Filtro por Nivel
**Entrada:**
```
Filtrar: ERROR
```
**Salida Esperada:**
- Solo líneas con [ERROR]
- Filtrado correcto

---

### 8. Pruebas de Persistencia

#### Caso 8.1: Reinicio del Sistema
**Secuencia:**
```
1. Crear herramienta H001
2. Cerrar sistema
3. Reiniciar sistema
4. Buscar H001
```
**Resultado:**
- H001 existe y mantiene todos los datos

#### Caso 8.2: Integridad Referencial
**Validación:**
```
- Préstamo P001 referencia a U001 y H001
- Eliminar U001 → No afecta historial de P001
- Usuario marcado como inactivo
```

---

## Datos de Ejemplo para Carga Inicial

### Herramientas
```
1. Taladro Eléctrico - Construcción - 3 unidades - $250,000
2. Cortadora de Césped - Jardinería - 2 unidades - $800,000
3. Escalera Extensible - Construcción - 2 unidades - $350,000
4. Compresor de Aire - Construcción - 1 unidad - $1,200,000
5. Motoguadaña - Jardinería - 2 unidades - $450,000
6. Sierra Circular - Construcción - 1 unidad - $380,000
7. Hidrolavadora - Limpieza - 1 unidad - $650,000
8. Carretilla - Jardinería - 4 unidades - $120,000
9. Taladro de Percusión - Construcción - 2 unidades - $320,000
10. Podadora de Setos - Jardinería - 1 unidad - $280,000
```

### Usuarios
```
1. admin - Administrador Sistema - 0000000000 - admin123
2. Juan Pérez - Residente - 3001234567 - juan123
3. María González - Residente - 3007654321 - maria123
4. Carlos Rodríguez - Residente - 3009876543 - carlos123
5. Ana Martínez - Residente - 3005432109 - ana123
```

### Escenarios de Préstamo
```
Activo:
- Juan tiene Taladro Eléctrico (vence en 2 días)
- María tiene Cortadora de Césped (vence hoy)

Vencido:
- Carlos tiene Escalera (vencido hace 3 días)

Historial:
- Ana devolvió Carretilla hace 1 semana (sin retraso)
- Juan devolvió Compresor hace 2 semanas (3 días de retraso)
```

---

## Comandos para Testing Rápido

```bash
# Limpiar datos de prueba
rm -rf datos/ logs/

# Ejecutar sistema
python main.py

# Credenciales por defecto
Usuario: admin
Password: admin123
```