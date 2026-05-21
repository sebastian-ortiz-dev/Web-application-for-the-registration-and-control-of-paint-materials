class Usuario(object):
    def __init__(self):
        pass

    def create_usuario(self, nombre, clave, nivel, imagen, fecha):
        query = "INSERT INTO usuario (nombre_usuario, clave, id_nivel, imagen_usu, fecha_creacion) VALUES (%s, %s, %s, %s, %s)"
        parametros = (nombre, clave, nivel, imagen, fecha)
        return query, parametros
        
    def modificar_usuario(self, nombre, clave, nivel, imagen, id):
        query = "UPDATE usuario SET nombre_usuario=%s, clave=%s, id_nivel=%s, imagen_usu=%s WHERE id_usuario = %s"
        parametros = (nombre, clave, nivel, imagen, id)
        return query, parametros
    
    def user_rehash(self, new_hash, id):
        query = "UPDATE usuario SET clave=%s WHERE id_usuario = %s"
        parametros = (new_hash, id)
        return query, parametros

    def eliminar_usuario(self, id):
        query = "UPDATE usuario SET borrado=%s WHERE id_usuario = %s"
        parametros = ("TRUE", id)
        return query, parametros
    
    def recuperar_usuario(self, id):
        query = "UPDATE usuario SET borrado=%s WHERE id_usuario = %s"
        parametros = ("False", id)
        return query, parametros

    def listar(self):
        return "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario u INNER JOIN niveles_acceso n ON u.id_nivel =  n.id_nivel WHERE u.borrado = FALSE"
    
    def listar_inactivo_perfil(self):
        return "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario u INNER JOIN niveles_acceso n ON u.id_nivel =  n.id_nivel WHERE u.borrado = TRUE"

    def contar_perfil_inactivo(self):
        return "SELECT COALESCE(COUNT(id_usuario),0) FROM usuario WHERE borrado = TRUE"

    def obtener_uno(self, id):
        query = "SELECT * FROM usuario INNER JOIN niveles_acceso ON usuario.id_nivel =  niveles_acceso.id_nivel WHERE id_usuario=%s"
        parametros = (id,)
        return query, parametros
    
    def obtener_uno_refresh(self, id):
        query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario u INNER JOIN niveles_acceso n ON u.id_nivel =  n.id_nivel WHERE u.borrado = False AND u.id_usuario=%s"
        parametros = (id,)
        return query, parametros
    
    def obtener_nombre(self, id):
        query = "SELECT nombre_usuario FROM usuario WHERE id_usuario=%s"
        parametros = (id,)
        return query, parametros

    def login(self, nombre):
        query = "SELECT usuario.id_usuario, usuario.nombre_usuario, usuario.clave, usuario.imagen_usu, niveles_acceso.nombre_nivel FROM usuario INNER JOIN niveles_acceso ON usuario.id_nivel = niveles_acceso.id_nivel WHERE nombre_usuario = %s"
        parametros = (nombre,)
        return query, parametros
    
    def busqueda_usuario(self, filtro):
        query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario as u INNER JOIN niveles_acceso as n ON u.id_nivel = n.id_nivel WHERE u.borrado = FALSE AND (u.id_usuario::text ILIKE %(busqueda)s OR u.nombre_usuario ILIKE %(busqueda)s)"
        parametros = {'busqueda': filtro}
        return query, parametros
    
    def busqueda_usuario_inactivo(self, filtro):
        query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario as u INNER JOIN niveles_acceso as n ON u.id_nivel = n.id_nivel WHERE u.borrado = TRUE AND (u.id_usuario::text ILIKE %(busqueda)s OR u.nombre_usuario ILIKE %(busqueda)s)"
        parametros = {'busqueda': filtro}
        return query, parametros
        
    def busqueda_usuario_acceso(self, filtro, categoria):
        query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario as u INNER JOIN niveles_acceso as n ON u.id_nivel = n.id_nivel WHERE u.borrado = FALSE AND u.id_nivel = %(categoria)s AND (u.id_usuario::text ILIKE %(busqueda)s OR u.nombre_usuario ILIKE %(busqueda)s)"
        parametros = {'categoria': categoria, 'busqueda': filtro}
        return query, parametros
        