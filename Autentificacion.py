"""
Módulo de Autenticación
"""

class Autenticacion:
    def __init__(self, gestion_usuarios, logger):
        self.usuarios = gestion_usuarios
        self.logger = logger
        self.sesion_activa = None
    
    def autenticar(self, id_usuario, password):
        """Autentica a un usuario"""
        usuario = self.usuarios.buscar_usuario(id_usuario)
        
        if not usuario:
            self.logger.registrar_evento("WARNING", f"Intento de acceso con ID inexistente: {id_usuario}")
            return {
                'exito': False,
                'mensaje': 'Usuario o contraseña incorrectos'
            }
        
        if not self.usuarios.verificar_password(id_usuario, password):
            self.logger.registrar_evento("WARNING", f"Intento de acceso fallido para usuario: {id_usuario}")
            return {
                'exito': False,
                'mensaje': 'Usuario o contraseña incorrectos'
            }
        
        self.sesion_activa = {
            'id_usuario': id_usuario,
            'tipo': usuario['tipo'],
            'nombres': usuario['nombres']
        }
        
        self.logger.registrar_evento("INFO", f"Usuario autenticado exitosamente: {id_usuario}")
        
        return {
            'exito': True,
            'tipo': usuario['tipo'],
            'nombres': usuario['nombres'],
            'id_usuario': id_usuario
        }
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        if self.sesion_activa:
            self.logger.registrar_evento("INFO", f"Sesión cerrada: {self.sesion_activa['id_usuario']}")
            self.sesion_activa = None
            return {'exito': True}
        return {'exito': False, 'mensaje': 'No hay sesión activa'}
    
    def obtener_sesion(self):
        """Obtiene información de la sesión actual"""
        return self.sesion_activa
    
    def es_administrador(self):
        """Verifica si el usuario actual es administrador"""
        if not self.sesion_activa:
            return False
        return self.sesion_activa['tipo'] == 'administrador'