"""
Módulo de Gestión de Usuarios
"""

import json
import os
import hashlib
from datetime import datetime

class GestionUsuarios:
    def __init__(self, logger):
        self.archivo = "datos/usuarios.json"
        self.logger = logger
        self.usuarios = self._cargar_datos()
        self._crear_directorio()
    
    def _crear_directorio(self):
        os.makedirs("datos", exist_ok=True)
    
    def _cargar_datos(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.registrar_evento("ERROR", f"Error al cargar usuarios: {str(e)}")
                return {}
        return {}
    
    def _guardar_datos(self):
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(self.usuarios, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.logger.registrar_evento("ERROR", f"Error al guardar usuarios: {str(e)}")
            return False
    
    def _generar_id(self):
        if not self.usuarios:
            return "U001"
        # Excluir el ID 'admin' del cálculo
        nums = [int(u_id[1:]) for u_id in self.usuarios.keys() if u_id != 'admin']
        if not nums:
            return "U001"
        ultimo_num = max(nums)
        return f"U{str(ultimo_num + 1).zfill(3)}"
    
    def _hash_password(self, password):
        """Hashea la contraseña para almacenamiento seguro"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def crear_usuario(self, nombres, apellidos, telefono, direccion, tipo, password):
        if not nombres or not apellidos or not password:
            return {'exito': False, 'mensaje': 'Datos obligatorios faltantes'}
        
        tipos_validos = ['residente', 'administrador']
        if tipo.lower() not in tipos_validos:
            return {'exito': False, 'mensaje': f'Tipo debe ser: {", ".join(tipos_validos)}'}
        
        # Generar ID especial para administrador si es el primero
        if tipo.lower() == 'administrador' and 'admin' not in self.usuarios:
            id_usuario = 'admin'
        else:
            id_usuario = self._generar_id()
        
        self.usuarios[id_usuario] = {
            'id': id_usuario,
            'nombres': nombres,
            'apellidos': apellidos,
            'telefono': telefono,
            'direccion': direccion,
            'tipo': tipo.lower(),
            'password': self._hash_password(password),
            'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'activo': True
        }
        
        if self._guardar_datos():
            return {'exito': True, 'id': id_usuario}
        return {'exito': False, 'mensaje': 'Error al guardar'}
    
    def listar_usuarios(self):
        return [u for u in self.usuarios.values() if u.get('activo', True)]
    
    def buscar_usuario(self, id_usuario):
        usuario = self.usuarios.get(id_usuario)
        if usuario and usuario.get('activo', True):
            return usuario
        return None
    
    def actualizar_usuario(self, id_usuario, nombres, apellidos, telefono, direccion, tipo):
        if id_usuario not in self.usuarios:
            return {'exito': False, 'mensaje': 'Usuario no encontrado'}
        
        tipos_validos = ['residente', 'administrador']
        if tipo.lower() not in tipos_validos:
            return {'exito': False, 'mensaje': f'Tipo debe ser: {", ".join(tipos_validos)}'}
        
        self.usuarios[id_usuario].update({
            'nombres': nombres,
            'apellidos': apellidos,
            'telefono': telefono,
            'direccion': direccion,
            'tipo': tipo.lower(),
            'fecha_actualizacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        if self._guardar_datos():
            return {'exito': True}
        return {'exito': False, 'mensaje': 'Error al guardar'}
    
    def eliminar_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            return {'exito': False, 'mensaje': 'Usuario no encontrado'}
        
        # Inactivar en lugar de eliminar para mantener integridad referencial
        self.usuarios[id_usuario]['activo'] = False
        self.usuarios[id_usuario]['fecha_eliminacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self._guardar_datos():
            return {'exito': True}
        return {'exito': False, 'mensaje': 'Error al guardar'}
    
    def verificar_password(self, id_usuario, password):
        """Verifica si la contraseña es correcta"""
        usuario = self.usuarios.get(id_usuario)
        if not usuario or not usuario.get('activo', True):
            return False
        
        return usuario.get('password') == self._hash_password(password)