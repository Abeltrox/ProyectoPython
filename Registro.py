"""
Módulo de Registro de Eventos (Logger)
"""

import os
from datetime import datetime

class Logger:
    def __init__(self, archivo="logs/sistema.log"):
        self.archivo = archivo
        self._crear_directorio()
    
    def _crear_directorio(self):
        """Crea el directorio de logs si no existe"""
        directorio = os.path.dirname(self.archivo)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
    
    def registrar_evento(self, nivel, mensaje):
        """
        Registra un evento en el archivo de logs
        
        Args:
            nivel: Nivel del evento (INFO, WARNING, ERROR, DEBUG)
            mensaje: Descripción del evento
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{timestamp}] [{nivel}] {mensaje}\n"
        
        try:
            with open(self.archivo, 'a', encoding='utf-8') as f:
                f.write(linea_log)
        except Exception as e:
            print(f"Error al escribir en el log: {str(e)}")
    
    def leer_logs(self, ultimas_lineas=None):
        """
        Lee el archivo de logs
        
        Args:
            ultimas_lineas: Si se especifica, retorna solo las últimas N líneas
        
        Returns:
            Lista de líneas del log
        """
        if not os.path.exists(self.archivo):
            return []
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                
                if ultimas_lineas:
                    return lineas[-ultimas_lineas:]
                return lineas
        except Exception as e:
            print(f"Error al leer el log: {str(e)}")
            return []
    
    def filtrar_por_nivel(self, nivel):
        """
        Retorna solo los eventos de un nivel específico
        
        Args:
            nivel: Nivel a filtrar (INFO, WARNING, ERROR, DEBUG)
        
        Returns:
            Lista de líneas filtradas
        """
        todas_lineas = self.leer_logs()
        return [linea for linea in todas_lineas if f"[{nivel}]" in linea]
    
    def filtrar_por_fecha(self, fecha):
        """
        Retorna solo los eventos de una fecha específica
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD
        
        Returns:
            Lista de líneas filtradas
        """
        todas_lineas = self.leer_logs()
        return [linea for linea in todas_lineas if fecha in linea]
    
    def limpiar_logs(self):
        """Limpia el archivo de logs"""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                f.write("")
            return True
        except Exception as e:
            print(f"Error al limpiar el log: {str(e)}")
            return False