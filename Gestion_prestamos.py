"""
Módulo de Gestión de Préstamos
"""

import json
import os
from datetime import datetime, timedelta

class GestionPrestamos:
    def __init__(self, logger):
        self.archivo_prestamos = "datos/prestamos.json"
        self.archivo_solicitudes = "datos/solicitudes.json"
        self.logger = logger
        self.prestamos = self._cargar_datos(self.archivo_prestamos)
        self.solicitudes = self._cargar_datos(self.archivo_solicitudes)
        self._crear_directorio()
    
    def _crear_directorio(self):
        os.makedirs("datos", exist_ok=True)
    
    def _cargar_datos(self, archivo):
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.registrar_evento("ERROR", f"Error al cargar {archivo}: {str(e)}")
                return {}
        return {}
    
    def _guardar_datos(self, archivo, datos):
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.logger.registrar_evento("ERROR", f"Error al guardar {archivo}: {str(e)}")
            return False
    
    def _generar_id(self, tipo='P'):
        if tipo == 'P':
            datos = self.prestamos
        else:
            datos = self.solicitudes
            
        if not datos:
            return f"{tipo}001"
        ultimo_num = max([int(p_id[1:]) for p_id in datos.keys()])
        return f"{tipo}{str(ultimo_num + 1).zfill(3)}"
    
    def crear_solicitud(self, id_usuario, id_herramienta, cantidad, dias_prestamo, observaciones=""):
        """Crea una solicitud de préstamo que debe ser aprobada por un administrador"""
        if cantidad <= 0 or dias_prestamo <= 0:
            return {'exito': False, 'mensaje': 'Cantidad y días deben ser positivos'}
        
        id_solicitud = self._generar_id('S')
        
        self.solicitudes[id_solicitud] = {
            'id': id_solicitud,
            'id_usuario': id_usuario,
            'id_herramienta': id_herramienta,
            'cantidad': cantidad,
            'dias_prestamo': dias_prestamo,
            'observaciones': observaciones,
            'estado': 'pendiente',
            'fecha_solicitud': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if self._guardar_datos(self.archivo_solicitudes, self.solicitudes):
            return {'exito': True, 'id': id_solicitud}
        return {'exito': False, 'mensaje': 'Error al guardar solicitud'}
    
    def listar_solicitudes_pendientes(self):
        """Lista todas las solicitudes pendientes de aprobación"""
        return [s for s in self.solicitudes.values() if s['estado'] == 'pendiente']
    
    def aprobar_solicitud(self, id_solicitud, gestion_herramientas):
        """Aprueba una solicitud y crea el préstamo"""
        if id_solicitud not in self.solicitudes:
            return {'exito': False, 'mensaje': 'Solicitud no encontrada'}
        
        solicitud = self.solicitudes[id_solicitud]
        
        if solicitud['estado'] != 'pendiente':
            return {'exito': False, 'mensaje': 'La solicitud ya fue procesada'}
        
        # Crear el préstamo
        resultado = self.crear_prestamo(
            solicitud['id_usuario'],
            solicitud['id_herramienta'],
            solicitud['cantidad'],
            solicitud['dias_prestamo'],
            solicitud['observaciones'],
            gestion_herramientas
        )
        
        if resultado['exito']:
            # Actualizar estado de la solicitud
            self.solicitudes[id_solicitud]['estado'] = 'aprobada'
            self.solicitudes[id_solicitud]['id_prestamo'] = resultado['id']
            self.solicitudes[id_solicitud]['fecha_aprobacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._guardar_datos(self.archivo_solicitudes, self.solicitudes)
            return {'exito': True, 'id': resultado['id']}
        
        return resultado
    
    def rechazar_solicitud(self, id_solicitud, motivo):
        """Rechaza una solicitud"""
        if id_solicitud not in self.solicitudes:
            return {'exito': False, 'mensaje': 'Solicitud no encontrada'}
        
        self.solicitudes[id_solicitud]['estado'] = 'rechazada'
        self.solicitudes[id_solicitud]['motivo_rechazo'] = motivo
        self.solicitudes[id_solicitud]['fecha_rechazo'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self._guardar_datos(self.archivo_solicitudes, self.solicitudes):
            return {'exito': True}
        return {'exito': False, 'mensaje': 'Error al guardar'}
    
    def crear_prestamo(self, id_usuario, id_herramienta, cantidad, dias_prestamo, observaciones, gestion_herramientas):
        """Crea un préstamo directamente (para administradores)"""
        if cantidad <= 0 or dias_prestamo <= 0:
            return {'exito': False, 'mensaje': 'Cantidad y días deben ser positivos'}
        
        # Verificar disponibilidad
        if not gestion_herramientas.verificar_disponibilidad(id_herramienta, cantidad):
            self.logger.registrar_evento("ERROR", 
                f"Intento de préstamo sin stock suficiente - Herramienta: {id_herramienta}, Cantidad: {cantidad}")
            return {'exito': False, 'mensaje': 'No hay suficiente stock disponible o la herramienta no está activa'}
        
        # Ajustar stock
        resultado_ajuste = gestion_herramientas.ajustar_cantidad(id_herramienta, -cantidad)
        if not resultado_ajuste['exito']:
            return resultado_ajuste
        
        id_prestamo = self._generar_id('P')
        fecha_inicio = datetime.now()
        fecha_devolucion = fecha_inicio + timedelta(days=dias_prestamo)
        
        self.prestamos[id_prestamo] = {
            'id': id_prestamo,
            'id_usuario': id_usuario,
            'id_herramienta': id_herramienta,
            'cantidad': cantidad,
            'fecha_inicio': fecha_inicio.strftime("%Y-%m-%d %H:%M:%S"),
            'fecha_devolucion_estimada': fecha_devolucion.strftime("%Y-%m-%d"),
            'estado': 'activo',
            'observaciones': observaciones
        }
        
        if self._guardar_datos(self.archivo_prestamos, self.prestamos):
            return {'exito': True, 'id': id_prestamo}
        
        # Revertir ajuste de stock si falla el guardado
        gestion_herramientas.ajustar_cantidad(id_herramienta, cantidad)
        return {'exito': False, 'mensaje': 'Error al guardar préstamo'}
    
    def registrar_devolucion(self, id_prestamo, observaciones_devolucion, gestion_herramientas):
        """Registra la devolución de una herramienta"""
        if id_prestamo not in self.prestamos:
            return {'exito': False, 'mensaje': 'Préstamo no encontrado'}
        
        prestamo = self.prestamos[id_prestamo]
        
        if prestamo['estado'] != 'activo':
            return {'exito': False, 'mensaje': 'El préstamo no está activo'}
        
        # Restaurar stock
        resultado_ajuste = gestion_herramientas.ajustar_cantidad(
            prestamo['id_herramienta'], 
            prestamo['cantidad']
        )
        
        if not resultado_ajuste['exito']:
            return resultado_ajuste
        
        self.prestamos[id_prestamo]['estado'] = 'devuelto'
        self.prestamos[id_prestamo]['fecha_devolucion_real'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.prestamos[id_prestamo]['observaciones_devolucion'] = observaciones_devolucion
        
        if self._guardar_datos(self.archivo_prestamos, self.prestamos):
            return {'exito': True}
        
        # Revertir ajuste si falla el guardado
        gestion_herramientas.ajustar_cantidad(prestamo['id_herramienta'], -prestamo['cantidad'])
        return {'exito': False, 'mensaje': 'Error al guardar devolución'}
    
    def listar_prestamos_activos(self):
        """Lista todos los préstamos activos"""
        return [p for p in self.prestamos.values() if p['estado'] == 'activo']
    
    def obtener_prestamos_usuario(self, id_usuario):
        """Obtiene todos los préstamos activos de un usuario"""
        return [p for p in self.prestamos.values() 
                if p['id_usuario'] == id_usuario and p['estado'] == 'activo']
    
    def obtener_proxima_devolucion(self, id_herramienta):
        """Obtiene la fecha de la próxima devolución de una herramienta"""
        prestamos_herramienta = [p for p in self.prestamos.values() 
                                if p['id_herramienta'] == id_herramienta and p['estado'] == 'activo']
        
        if not prestamos_herramienta:
            return None
        
        fechas = [p['fecha_devolucion_estimada'] for p in prestamos_herramienta]
        return min(fechas)
    
    def obtener_historial_completo(self):
        """Obtiene todos los préstamos (activos y devueltos)"""
        return list(self.prestamos.values())