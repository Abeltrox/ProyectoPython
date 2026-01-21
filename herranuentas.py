"""
Sistema de Gestión de Herramientas Comunitarias
Archivo principal - main.py
"""
import Gestion_herramientas
import Gestion_usuario
import Gestion_prestamos
import Autentificacion
import Consultas
import Registro
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione ENTER para continuar...")

def menu_administrador(auth, herramientas, usuarios, prestamos, consultas, logger):
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("MENÚ ADMINISTRADOR".center(60))
        print("=" * 60)
        print("1.  Gestión de Herramientas")
        print("2.  Gestión de Usuarios")
        print("3.  Gestión de Préstamos")
        print("4.  Consultas e Informes")
        print("5.  Cerrar Sesión")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            menu_herramientas(herramientas, logger)
        elif opcion == "2":
            menu_usuarios(usuarios, logger)
        elif opcion == "3":
            menu_prestamos_admin(prestamos, herramientas, usuarios, logger)
        elif opcion == "4":
            menu_consultas(consultas, usuarios, herramientas)
        elif opcion == "5":
            logger.registrar_evento("INFO", f"Administrador cerró sesión")
            break
        else:
            print("Opción no válida")
            pausar()

def menu_usuario(auth, herramientas, usuarios, prestamos, consultas, logger, usuario_id):
    while True:
        limpiar_pantalla()
        usuario = usuarios.buscar_usuario(usuario_id)
        print("=" * 60)
        print(f"MENÚ USUARIO - {usuario['nombres']} {usuario['apellidos']}".center(60))
        print("=" * 60)
        print("1.  Consultar Herramientas Disponibles")
        print("2.  Ver Mis Préstamos Activos")
        print("3.  Solicitar Préstamo de Herramienta")
        print("4.  Cerrar Sesión")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            consultar_herramientas_usuario(herramientas, prestamos)
        elif opcion == "2":
            ver_mis_prestamos(prestamos, herramientas, usuario_id)
        elif opcion == "3":
            solicitar_prestamo_usuario(prestamos, herramientas, usuarios, logger, usuario_id)
        elif opcion == "4":
            logger.registrar_evento("INFO", f"Usuario {usuario['nombres']} cerró sesión")
            break
        else:
            print("Opción no válida")
            pausar()

def menu_herramientas(herramientas, logger):
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("GESTIÓN DE HERRAMIENTAS".center(60))
        print("=" * 60)
        print("1.  Crear Nueva Herramienta")
        print("2.  Listar Todas las Herramientas")
        print("3.  Buscar Herramienta")
        print("4.  Actualizar Herramienta")
        print("5.  Eliminar/Inactivar Herramienta")
        print("6.  Volver")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            crear_herramienta(herramientas, logger)
        elif opcion == "2":
            listar_herramientas(herramientas)
        elif opcion == "3":
            buscar_herramienta(herramientas)
        elif opcion == "4":
            actualizar_herramienta(herramientas, logger)
        elif opcion == "5":
            eliminar_herramienta(herramientas, logger)
        elif opcion == "6":
            break
        else:
            print("Opción no válida")
            pausar()

def crear_herramienta(herramientas, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("CREAR NUEVA HERRAMIENTA".center(60))
    print("=" * 60)
    
    nombre = input("Nombre de la herramienta: ").strip()
    categoria = input("Categoría (construcción/jardinería/otro): ").strip()
    try:
        cantidad = int(input("Cantidad disponible: "))
        valor = float(input("Valor estimado: "))
    except ValueError:
        print("Error: Valores numéricos inválidos")
        logger.registrar_evento("ERROR", "Intento de crear herramienta con valores inválidos")
        pausar()
        return
    
    estado = input("Estado (activa/en reparación/fuera de servicio): ").strip()
    
    resultado = herramientas.crear_herramienta(nombre, categoria, cantidad, estado, valor)
    if resultado['exito']:
        print(f"\n✓ Herramienta creada exitosamente con ID: {resultado['id']}")
        logger.registrar_evento("INFO", f"Herramienta creada: {nombre} (ID: {resultado['id']})")
    else:
        print(f"\n✗ Error: {resultado['mensaje']}")
        logger.registrar_evento("ERROR", f"Error al crear herramienta: {resultado['mensaje']}")
    
    pausar()

def listar_herramientas(herramientas):
    limpiar_pantalla()
    print("=" * 60)
    print("LISTADO DE HERRAMIENTAS".center(60))
    print("=" * 60)
    
    lista = herramientas.listar_herramientas()
    if not lista:
        print("No hay herramientas registradas")
    else:
        for h in lista:
            print(f"\nID: {h['id']}")
            print(f"Nombre: {h['nombre']}")
            print(f"Categoría: {h['categoria']}")
            print(f"Cantidad: {h['cantidad']}")
            print(f"Estado: {h['estado']}")
            print(f"Valor: ${h['valor']:,.2f}")
            print("-" * 60)
    
    pausar()

def buscar_herramienta(herramientas):
    limpiar_pantalla()
    print("=" * 60)
    print("BUSCAR HERRAMIENTA".center(60))
    print("=" * 60)
    
    criterio = input("Buscar por (1=ID, 2=Nombre, 3=Categoría): ").strip()
    valor = input("Ingrese el valor de búsqueda: ").strip()
    
    if criterio == "1":
        resultado = herramientas.buscar_herramienta(valor)
        if resultado:
            print(f"\nID: {resultado['id']}")
            print(f"Nombre: {resultado['nombre']}")
            print(f"Categoría: {resultado['categoria']}")
            print(f"Cantidad: {resultado['cantidad']}")
            print(f"Estado: {resultado['estado']}")
            print(f"Valor: ${resultado['valor']:,.2f}")
        else:
            print("Herramienta no encontrada")
    else:
        campo = 'nombre' if criterio == '2' else 'categoria'
        resultados = herramientas.buscar_por_campo(campo, valor)
        if resultados:
            for h in resultados:
                print(f"\nID: {h['id']} - {h['nombre']} ({h['categoria']}) - Stock: {h['cantidad']}")
        else:
            print("No se encontraron herramientas")
    
    pausar()

def actualizar_herramienta(herramientas, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("ACTUALIZAR HERRAMIENTA".center(60))
    print("=" * 60)
    
    id_herramienta = input("ID de la herramienta a actualizar: ").strip()
    herramienta = herramientas.buscar_herramienta(id_herramienta)
    
    if not herramienta:
        print("Herramienta no encontrada")
        pausar()
        return
    
    print(f"\nActualizando: {herramienta['nombre']}")
    print("Deje en blanco para mantener el valor actual\n")
    
    nombre = input(f"Nombre [{herramienta['nombre']}]: ").strip() or herramienta['nombre']
    categoria = input(f"Categoría [{herramienta['categoria']}]: ").strip() or herramienta['categoria']
    cantidad = input(f"Cantidad [{herramienta['cantidad']}]: ").strip()
    cantidad = int(cantidad) if cantidad else herramienta['cantidad']
    estado = input(f"Estado [{herramienta['estado']}]: ").strip() or herramienta['estado']
    valor = input(f"Valor [{herramienta['valor']}]: ").strip()
    valor = float(valor) if valor else herramienta['valor']
    
    resultado = herramientas.actualizar_herramienta(id_herramienta, nombre, categoria, cantidad, estado, valor)
    if resultado['exito']:
        print("\n✓ Herramienta actualizada exitosamente")
        logger.registrar_evento("INFO", f"Herramienta actualizada: {nombre} (ID: {id_herramienta})")
    else:
        print(f"\n✗ Error: {resultado['mensaje']}")
        logger.registrar_evento("ERROR", f"Error al actualizar herramienta: {resultado['mensaje']}")
    
    pausar()

def eliminar_herramienta(herramientas, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("ELIMINAR/INACTIVAR HERRAMIENTA".center(60))
    print("=" * 60)
    
    id_herramienta = input("ID de la herramienta: ").strip()
    confirmacion = input("¿Está seguro? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        resultado = herramientas.eliminar_herramienta(id_herramienta)
        if resultado['exito']:
            print("\n✓ Herramienta eliminada exitosamente")
            logger.registrar_evento("INFO", f"Herramienta eliminada: ID {id_herramienta}")
        else:
            print(f"\n✗ Error: {resultado['mensaje']}")
            logger.registrar_evento("ERROR", f"Error al eliminar herramienta: {resultado['mensaje']}")
    
    pausar()

def menu_usuarios(usuarios, logger):
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("GESTIÓN DE USUARIOS".center(60))
        print("=" * 60)
        print("1.  Crear Nuevo Usuario")
        print("2.  Listar Todos los Usuarios")
        print("3.  Buscar Usuario")
        print("4.  Actualizar Usuario")
        print("5.  Eliminar Usuario")
        print("6.  Volver")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            crear_usuario(usuarios, logger)
        elif opcion == "2":
            listar_usuarios(usuarios)
        elif opcion == "3":
            buscar_usuario(usuarios)
        elif opcion == "4":
            actualizar_usuario(usuarios, logger)
        elif opcion == "5":
            eliminar_usuario(usuarios, logger)
        elif opcion == "6":
            break
        else:
            print("Opción no válida")
            pausar()

def crear_usuario(usuarios, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("CREAR NUEVO USUARIO".center(60))
    print("=" * 60)
    
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    telefono = input("Teléfono: ").strip()
    direccion = input("Dirección: ").strip()
    tipo = input("Tipo de usuario (residente/administrador): ").strip()
    password = input("Contraseña: ").strip()
    
    resultado = usuarios.crear_usuario(nombres, apellidos, telefono, direccion, tipo, password)
    if resultado['exito']:
        print(f"\n✓ Usuario creado exitosamente con ID: {resultado['id']}")
        logger.registrar_evento("INFO", f"Usuario creado: {nombres} {apellidos} (ID: {resultado['id']})")
    else:
        print(f"\n✗ Error: {resultado['mensaje']}")
        logger.registrar_evento("ERROR", f"Error al crear usuario: {resultado['mensaje']}")
    
    pausar()

def listar_usuarios(usuarios):
    limpiar_pantalla()
    print("=" * 60)
    print("LISTADO DE USUARIOS".center(60))
    print("=" * 60)
    
    lista = usuarios.listar_usuarios()
    if not lista:
        print("No hay usuarios registrados")
    else:
        for u in lista:
            print(f"\nID: {u['id']}")
            print(f"Nombre: {u['nombres']} {u['apellidos']}")
            print(f"Teléfono: {u['telefono']}")
            print(f"Dirección: {u['direccion']}")
            print(f"Tipo: {u['tipo']}")
            print("-" * 60)
    
    pausar()

def buscar_usuario(usuarios):
    limpiar_pantalla()
    print("=" * 60)
    print("BUSCAR USUARIO".center(60))
    print("=" * 60)
    
    id_usuario = input("ID del usuario: ").strip()
    usuario = usuarios.buscar_usuario(id_usuario)
    
    if usuario:
        print(f"\nID: {usuario['id']}")
        print(f"Nombre: {usuario['nombres']} {usuario['apellidos']}")
        print(f"Teléfono: {usuario['telefono']}")
        print(f"Dirección: {usuario['direccion']}")
        print(f"Tipo: {usuario['tipo']}")
    else:
        print("Usuario no encontrado")
    
    pausar()

def actualizar_usuario(usuarios, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("ACTUALIZAR USUARIO".center(60))
    print("=" * 60)
    
    id_usuario = input("ID del usuario a actualizar: ").strip()
    usuario = usuarios.buscar_usuario(id_usuario)
    
    if not usuario:
        print("Usuario no encontrado")
        pausar()
        return
    
    print(f"\nActualizando: {usuario['nombres']} {usuario['apellidos']}")
    print("Deje en blanco para mantener el valor actual\n")
    
    nombres = input(f"Nombres [{usuario['nombres']}]: ").strip() or usuario['nombres']
    apellidos = input(f"Apellidos [{usuario['apellidos']}]: ").strip() or usuario['apellidos']
    telefono = input(f"Teléfono [{usuario['telefono']}]: ").strip() or usuario['telefono']
    direccion = input(f"Dirección [{usuario['direccion']}]: ").strip() or usuario['direccion']
    tipo = input(f"Tipo [{usuario['tipo']}]: ").strip() or usuario['tipo']
    
    resultado = usuarios.actualizar_usuario(id_usuario, nombres, apellidos, telefono, direccion, tipo)
    if resultado['exito']:
        print("\n✓ Usuario actualizado exitosamente")
        logger.registrar_evento("INFO", f"Usuario actualizado: {nombres} {apellidos} (ID: {id_usuario})")
    else:
        print(f"\n✗ Error: {resultado['mensaje']}")
        logger.registrar_evento("ERROR", f"Error al actualizar usuario: {resultado['mensaje']}")
    
    pausar()

def eliminar_usuario(usuarios, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("ELIMINAR USUARIO".center(60))
    print("=" * 60)
    
    id_usuario = input("ID del usuario: ").strip()
    confirmacion = input("¿Está seguro? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        resultado = usuarios.eliminar_usuario(id_usuario)
        if resultado['exito']:
            print("\n✓ Usuario eliminado exitosamente")
            logger.registrar_evento("INFO", f"Usuario eliminado: ID {id_usuario}")
        else:
            print(f"\n✗ Error: {resultado['mensaje']}")
            logger.registrar_evento("ERROR", f"Error al eliminar usuario: {resultado['mensaje']}")
    
    pausar()

def menu_prestamos_admin(prestamos, herramientas, usuarios, logger):
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("GESTIÓN DE PRÉSTAMOS".center(60))
        print("=" * 60)
        print("1.  Aprobar Solicitudes Pendientes")
        print("2.  Registrar Nuevo Préstamo")
        print("3.  Registrar Devolución")
        print("4.  Listar Préstamos Activos")
        print("5.  Volver")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            aprobar_solicitudes(prestamos, herramientas, usuarios, logger)
        elif opcion == "2":
            registrar_prestamo(prestamos, herramientas, usuarios, logger)
        elif opcion == "3":
            registrar_devolucion(prestamos, herramientas, logger)
        elif opcion == "4":
            listar_prestamos_activos(prestamos, herramientas, usuarios)
        elif opcion == "5":
            break
        else:
            print("Opción no válida")
            pausar()

def aprobar_solicitudes(prestamos, herramientas, usuarios, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("APROBAR SOLICITUDES PENDIENTES".center(60))
    print("=" * 60)
    
    solicitudes = prestamos.listar_solicitudes_pendientes()
    
    if not solicitudes:
        print("No hay solicitudes pendientes")
        pausar()
        return
    
    for sol in solicitudes:
        usuario = usuarios.buscar_usuario(sol['id_usuario'])
        herramienta = herramientas.buscar_herramienta(sol['id_herramienta'])
        
        print(f"\nSolicitud ID: {sol['id']}")
        print(f"Usuario: {usuario['nombres']} {usuario['apellidos']}")
        print(f"Herramienta: {herramienta['nombre']}")
        print(f"Cantidad: {sol['cantidad']}")
        print(f"Días solicitados: {sol['dias_prestamo']}")
        print(f"Observaciones: {sol['observaciones']}")
        print("-" * 60)
        
        accion = input("¿Aprobar esta solicitud? (s/n/c=cancelar): ").strip().lower()
        
        if accion == 's':
            resultado = prestamos.aprobar_solicitud(sol['id'], herramientas)
            if resultado['exito']:
                print("✓ Solicitud aprobada")
                logger.registrar_evento("INFO", f"Solicitud {sol['id']} aprobada")
            else:
                print(f"✗ Error: {resultado['mensaje']}")
                logger.registrar_evento("ERROR", f"Error al aprobar solicitud {sol['id']}: {resultado['mensaje']}")
        elif accion == 'n':
            motivo = input("Motivo del rechazo: ").strip()
            resultado = prestamos.rechazar_solicitud(sol['id'], motivo)
            if resultado['exito']:
                print("✓ Solicitud rechazada")
                logger.registrar_evento("INFO", f"Solicitud {sol['id']} rechazada: {motivo}")
        elif accion == 'c':
            break
    
    pausar()

def registrar_prestamo(prestamos, herramientas, usuarios, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("REGISTRAR NUEVO PRÉSTAMO".center(60))
    print("=" * 60)
    
    id_usuario = input("ID del usuario: ").strip()
    id_herramienta = input("ID de la herramienta: ").strip()
    
    try:
        cantidad = int(input("Cantidad a prestar: "))
        dias = int(input("Días de préstamo: "))
    except ValueError:
        print("Error: Valores numéricos inválidos")
        logger.registrar_evento("ERROR", "Intento de préstamo con valores inválidos")
        pausar()
        return
    
    observaciones = input("Observaciones: ").strip()
    
    resultado = prestamos.crear_prestamo(id_usuario, id_herramienta, cantidad, dias, observaciones, herramientas)
    if resultado['exito']:
        print(f"\n✓ Préstamo registrado exitosamente con ID: {resultado['id']}")
        logger.registrar_evento("INFO", f"Préstamo creado: ID {resultado['id']}")
    else:
        print(f"\n✗ Error: {resultado['mensaje']}")
        logger.registrar_evento("ERROR", f"Error al crear préstamo: {resultado['mensaje']}")
    
    pausar()

def registrar_devolucion(prestamos, herramientas, logger):
    limpiar_pantalla()
    print("=" * 60)
    print("REGISTRAR DEVOLUCIÓN".center(60))
    print("=" * 60)
    
    id_prestamo = input("ID del préstamo: ").strip()
    observaciones = input("Observaciones de la devolución: ").strip()
    
    resultado = prestamos.registrar_devolucion(id_prestamo, observaciones, herramientas)
    if resultado['exito']:
        print("\n✓ Devolución registrada exitosamente")
        logger.registrar_evento("INFO", f"Devolución registrada: Préstamo ID {id_prestamo}")
    else:
        print(f"\n✗ Error: {resultado['mensaje']}")
        logger.registrar_evento("ERROR", f"Error al registrar devolución: {resultado['mensaje']}")
    
    pausar()

def listar_prestamos_activos(prestamos, herramientas, usuarios):
    limpiar_pantalla()
    print("=" * 60)
    print("PRÉSTAMOS ACTIVOS".center(60))
    print("=" * 60)
    
    lista = prestamos.listar_prestamos_activos()
    
    if not lista:
        print("No hay préstamos activos")
    else:
        for p in lista:
            usuario = usuarios.buscar_usuario(p['id_usuario'])
            herramienta = herramientas.buscar_herramienta(p['id_herramienta'])
            
            print(f"\nPréstamo ID: {p['id']}")
            print(f"Usuario: {usuario['nombres']} {usuario['apellidos']}")
            print(f"Herramienta: {herramienta['nombre']}")
            print(f"Cantidad: {p['cantidad']}")
            print(f"Fecha inicio: {p['fecha_inicio']}")
            print(f"Fecha estimada devolución: {p['fecha_devolucion_estimada']}")
            print(f"Estado: {p['estado']}")
            print("-" * 60)
    
    pausar()

def consultar_herramientas_usuario(herramientas, prestamos):
    limpiar_pantalla()
    print("=" * 60)
    print("HERRAMIENTAS DISPONIBLES".center(60))
    print("=" * 60)
    
    lista = herramientas.listar_herramientas()
    
    for h in lista:
        if h['estado'] == 'activa' and h['cantidad'] > 0:
            print(f"\nID: {h['id']}")
            print(f"Nombre: {h['nombre']}")
            print(f"Categoría: {h['categoria']}")
            print(f"Cantidad disponible: {h['cantidad']}")
            print("-" * 60)
        elif h['cantidad'] == 0:
            # Buscar cuándo estará disponible
            proxima_devolucion = prestamos.obtener_proxima_devolucion(h['id'])
            if proxima_devolucion:
                print(f"\nID: {h['id']}")
                print(f"Nombre: {h['nombre']}")
                print(f"Categoría: {h['categoria']}")
                print(f"NO DISPONIBLE - Próxima devolución: {proxima_devolucion}")
                print("-" * 60)
    
    pausar()

def ver_mis_prestamos(prestamos, herramientas, usuario_id):
    limpiar_pantalla()
    print("=" * 60)
    print("MIS PRÉSTAMOS ACTIVOS".center(60))
    print("=" * 60)
    
    lista = prestamos.obtener_prestamos_usuario(usuario_id)
    
    if not lista:
        print("No tiene préstamos activos")
    else:
        for p in lista:
            herramienta = herramientas.buscar_herramienta(p['id_herramienta'])
            print(f"\nPréstamo ID: {p['id']}")
            print(f"Herramienta: {herramienta['nombre']}")
            print(f"Cantidad: {p['cantidad']}")
            print(f"Fecha inicio: {p['fecha_inicio']}")
            print(f"Fecha estimada devolución: {p['fecha_devolucion_estimada']}")
            print(f"Estado: {p['estado']}")
            print("-" * 60)
    
    pausar()

def solicitar_prestamo_usuario(prestamos, herramientas, usuarios, logger, usuario_id):
    limpiar_pantalla()
    print("=" * 60)
    print("SOLICITAR PRÉSTAMO DE HERRAMIENTA".center(60))
    print("=" * 60)
    
    id_herramienta = input("ID de la herramienta: ").strip()
    herramienta = herramientas.buscar_herramienta(id_herramienta)
    
    if not herramienta:
        print("Herramienta no encontrada")
        pausar()
        return
    
    print(f"\nHerramienta: {herramienta['nombre']}")
    print(f"Disponibles: {herramienta['cantidad']}")
    
    try:
        cantidad = int(input("Cantidad a solicitar: "))
        dias = int(input("Días de préstamo: "))
    except ValueError:
        print("Error: Valores numéricos inválidos")
        pausar()
        return
    
    observaciones = input("Observaciones (opcional): ").strip()
    
    resultado = prestamos.crear_solicitud(usuario_id, id_herramienta, cantidad, dias, observaciones)
    if resultado['exito']:
        print(f"\n✓ Solicitud creada exitosamente. ID: {resultado['id']}")
        print("Su solicitud será revisada por un administrador")
        logger.registrar_evento("INFO", f"Solicitud de préstamo creada por usuario {usuario_id}")
    else:
        print(f"\n✗ Error: {resultado['mensaje']}")
        logger.registrar_evento("ERROR", f"Error al crear solicitud: {resultado['mensaje']}")
    
    pausar()

def menu_consultas(consultas, usuarios, herramientas):
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("CONSULTAS E INFORMES".center(60))
        print("=" * 60)
        print("1.  Herramientas con Stock Bajo")
        print("2.  Préstamos Activos")
        print("3.  Préstamos Vencidos")
        print("4.  Historial de Préstamos de un Usuario")
        print("5.  Herramientas Más Solicitadas")
        print("6.  Usuarios con Más Préstamos")
        print("7.  Volver")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            mostrar_stock_bajo(consultas, herramientas)
        elif opcion == "2":
            mostrar_prestamos_activos(consultas, usuarios, herramientas)
        elif opcion == "3":
            mostrar_prestamos_vencidos(consultas, usuarios, herramientas)
        elif opcion == "4":
            mostrar_historial_usuario(consultas, usuarios, herramientas)
        elif opcion == "5":
            mostrar_herramientas_solicitadas(consultas, herramientas)
        elif opcion == "6":
            mostrar_usuarios_activos(consultas, usuarios)
        elif opcion == "7":
            break
        else:
            print("Opción no válida")
            pausar()

def mostrar_stock_bajo(consultas, herramientas):
    limpiar_pantalla()
    print("=" * 60)
    print("HERRAMIENTAS CON STOCK BAJO".center(60))
    print("=" * 60)
    
    limite = int(input("Límite de stock (por defecto 3): ").strip() or "3")
    lista = consultas.herramientas_stock_bajo(limite)
    
    if not lista:
        print(f"No hay herramientas con stock menor a {limite}")
    else:
        for h_id in lista:
            h = herramientas.buscar_herramienta(h_id)
            print(f"\n{h['nombre']} - Stock: {h['cantidad']}")
    
    pausar()

def mostrar_prestamos_activos(consultas, usuarios, herramientas):
    limpiar_pantalla()
    print("=" * 60)
    print("PRÉSTAMOS ACTIVOS".center(60))
    print("=" * 60)
    
    lista = consultas.prestamos_activos()
    
    if not lista:
        print("No hay préstamos activos")
    else:
        for p in lista:
            u = usuarios.buscar_usuario(p['id_usuario'])
            h = herramientas.buscar_herramienta(p['id_herramienta'])
            print(f"\nPréstamo ID: {p['id']}")
            print(f"Usuario: {u['nombres']} {u['apellidos']}")
            print(f"Herramienta: {h['nombre']}")
            print(f"Vence: {p['fecha_devolucion_estimada']}")
            print("-" * 60)
    
    pausar()

def mostrar_prestamos_vencidos(consultas, usuarios, herramientas):
    limpiar_pantalla()
    print("=" * 60)
    print("PRÉSTAMOS VENCIDOS".center(60))
    print("=" * 60)
    
    lista = consultas.prestamos_vencidos()
    
    if not lista:
        print("No hay préstamos vencidos")
    else:
        for p in lista:
            u = usuarios.buscar_usuario(p['id_usuario'])
            h = herramientas.buscar_herramienta(p['id_herramienta'])
            print(f"\nPréstamo ID: {p['id']}")
            print(f"Usuario: {u['nombres']} {u['apellidos']} - Tel: {u['telefono']}")
            print(f"Herramienta: {h['nombre']}")
            print(f"Vencido desde: {p['fecha_devolucion_estimada']}")
            print("-" * 60)
    
    pausar()

def mostrar_historial_usuario(consultas, usuarios, herramientas):
    limpiar_pantalla()
    print("=" * 60)
    print("HISTORIAL DE PRÉSTAMOS DE USUARIO".center(60))
    print("=" * 60)
    
    id_usuario = input("ID del usuario: ").strip()
    u = usuarios.buscar_usuario(id_usuario)
    
    if not u:
        print("Usuario no encontrado")
        pausar()
        return
    
    print(f"\nUsuario: {u['nombres']} {u['apellidos']}\n")
    
    historial = consultas.historial_usuario(id_usuario)
    
    if not historial:
        print("No hay historial de préstamos")
    else:
        for p in historial:
            h = herramientas.buscar_herramienta(p['id_herramienta'])
            print(f"ID: {p['id']} - {h['nombre']} - Estado: {p['estado']}")
            print(f"Inicio: {p['fecha_inicio']} | Devolución: {p.get('fecha_devolucion_real', 'Pendiente')}")
            print("-" * 60)
    
    pausar()

def mostrar_herramientas_solicitadas(consultas, herramientas):
    limpiar_pantalla()
    print("=" * 60)
    print("HERRAMIENTAS MÁS SOLICITADAS".center(60))
    print("=" * 60)
    
    ranking = consultas.herramientas_mas_solicitadas()
    
    if not ranking:
        print("No hay datos suficientes")
    else:
        print("\nRanking de herramientas más solicitadas:\n")
        for i, (h_id, cantidad) in enumerate(ranking, 1):
            h = herramientas.buscar_herramienta(h_id)
            print(f"{i}. {h['nombre']} - {cantidad} préstamos")
    
    pausar()

def mostrar_usuarios_activos(consultas, usuarios):
    limpiar_pantalla()
    print("=" * 60)
    print("USUARIOS CON MÁS PRÉSTAMOS".center(60))
    print("=" * 60)
    
    ranking = consultas.usuarios_mas_activos()
    
    if not ranking:
        print("No hay datos suficientes")
    else:
        print("\nRanking de usuarios más activos:\n")
        for i, (u_id, cantidad) in enumerate(ranking, 1):
            u = usuarios.buscar_usuario(u_id)
            print(f"{i}. {u['nombres']} {u['apellidos']} - {cantidad} préstamos")
    
    pausar()

def herranuentas():
    # Inicializar componentes
    logger = Registro()
    herramientas = Gestion_herramientas(Registro)
    usuarios = Gestion_usuario(Registro)
    prestamos = Gestion_prestamos(Registro)
    auth = Autentificacion(usuarios, Registro)
    consultas = Consultas(prestamos, Registro)
    
    logger.registrar_evento("INFO", "Sistema iniciado")
    
    # Crear usuario administrador por defecto si no existe
    if not usuarios.buscar_usuario("admin"):
        usuarios.crear_usuario("Administrador", "Sistema", "0000000000", "N/A", "administrador", "admin123")
        logger.registrar_evento("INFO", "Usuario administrador creado por defecto")
    
    while True:
        limpiar_pantalla()
        print("=" * 60)
        print("SISTEMA DE GESTIÓN DE HERRAMIENTAS COMUNITARIAS".center(60))
        print("=" * 60)
        print("1.  Iniciar Sesión")
        print("2.  Salir")
        print("=" * 60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            print("=" * 60)
            print("INICIO DE SESIÓN".center(60))
            print("=" * 60)
            id_usuario = input("ID de usuario: ").strip()
            password = input("Contraseña: ").strip()
            
            resultado = auth.autenticar(id_usuario, password)
            
            if resultado['exito']:
                tipo_usuario = resultado['tipo']
                print(f"\n✓ Bienvenido {resultado['nombres']}")
                pausar()
                
                if tipo_usuario == "administrador":
                    menu_administrador(auth, herramientas, usuarios, prestamos, consultas, logger)
                else:
                    menu_usuario(auth, herramientas, usuarios, prestamos, consultas, logger, id_usuario)
            else:
                print(f"\n✗ {resultado['mensaje']}")
                pausar()
        
        elif opcion == "2":
            logger.registrar_evento("INFO", "Sistema cerrado")
            print("\n¡Hasta pronto!")
            break
        else:
            print("Opción no válida")
            pausar()

if __name__ == "__main__":
    herranuentas()