class Proveedor(object):
    def __init__(self):
        pass

    def create_proveedor(self, nombre, correo, direccion, telefono, rif, fecha):
        query = "INSERT INTO distribuidor (nombre, correo, direccion, telefono, rif, borrado, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        parametros = (nombre, correo, direccion, telefono, rif, 'false', fecha)
        return query, parametros
        
    def modificar_proveedor(self, id, nombre, correo, direccion, telefono, rif):
        query = "UPDATE distribuidor SET nombre=%s, correo=%s, direccion=%s, telefono=%s, rif=%s WHERE id_distribuidor=%s"
        parametros = (nombre, correo, direccion, telefono, rif, id)
        return query, parametros

    def eliminar_proveedor(self, id):
        query = "UPDATE distribuidor set borrado=%s WHERE id_distribuidor= %s"
        parametros = ("TRUE", id)
        return query, parametros
    
    def recuperar_proveedor(self, id):
        query = "UPDATE distribuidor set borrado=%s WHERE id_distribuidor= %s"
        parametros = ("FALSE", id)
        return query, parametros
            
    def listar(self):
        return "SELECT * FROM distribuidor WHERE borrado = FALSE ORDER BY id_distribuidor ASC"
    
    def listar_inactivo(self):
        return "SELECT * FROM distribuidor WHERE borrado = TRUE ORDER BY id_distribuidor ASC"

    def listar_varios(self):
        return "SELECT id_distribuidor, nombre FROM distribuidor WHERE borrado = FALSE"
    
    def listar_id(self):
        return "SELECT id_distribuidor FROM distribuidor WHERE borrado = FALSE"
    
    def contar_proveedor(self):
        return "SELECT COUNT(id_distribuidor) FROM distribuidor WHERE borrado = TRUE"
    
    def contar_inactivo(self):
        return "SELECT COALESCE(COUNT(id_distribuidor),0) FROM distribuidor WHERE borrado = TRUE"

    def obtener_uno(self, id):
        query = "SELECT * FROM distribuidor WHERE id_distribuidor=%s "
        parametros = (id,)
        return query, parametros
    
    def obtener_un_proveedor(self, id):
        query = "SELECT id_distribuidor, nombre FROM distribuidor WHERE id_distribuidor=%s and borrado = FALSE"
        parametros = (id,)
        return query, parametros
    
    def obtener_proveedores(self, id_lista):
        query = "SELECT id_distribuidor, nombre FROM distribuidor WHERE id_distribuidor in %s ORDER BY id_distribuidor ASC"
        parametros = (id_lista,)
        return query, parametros

    def busqueda_proveedor(self, filtro):
        query = "SELECT * FROM distribuidor WHERE borrado = FALSE AND (id_distribuidor::text ILIKE %(busqueda)s OR nombre ILIKE %(busqueda)s OR correo ILIKE %(busqueda)s OR direccion ILIKE %(busqueda)s OR telefono ILIKE %(busqueda)s OR rif ILIKE %(busqueda)s OR fecha_registro::text ILIKE %(busqueda)s) ORDER BY id_distribuidor ASC"
        parametros = {'busqueda': filtro}
        return query, parametros
    
    def busqueda_proveedor_inactivo(self, filtro):
        query = "SELECT * FROM distribuidor WHERE borrado = TRUE AND (id_distribuidor::text ILIKE %(busqueda)s OR nombre ILIKE %(busqueda)s OR correo ILIKE %(busqueda)s OR direccion ILIKE %(busqueda)s OR telefono ILIKE %(busqueda)s OR rif ILIKE %(busqueda)s OR fecha_registro::text ILIKE %(busqueda)s) ORDER BY id_distribuidor ASC"
        parametros = {'busqueda': filtro}
        return query, parametros