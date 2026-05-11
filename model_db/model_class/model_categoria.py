class Categoria(object):
    def __init__(self):
        pass

    def crear(self, nombre):
        query = "INSERT INTO categorias (categoria) VALUES (%s)"
        parametros = (nombre,)
        return query, parametros
    
    def modificar(self, nombre, id):
        query = "UPDATE categorias SET categoria=%s WHERE id_categoria = %s"
        parametro = (nombre, id)
        return query, parametro

    def listar(self):
        return "SELECT * FROM categorias"
    
    def obtener_uno(self, id):
        query = "SELECT * FROM categorias WHERE id_categoria = %s"
        parametro = (id,)
        return query, parametro
    

