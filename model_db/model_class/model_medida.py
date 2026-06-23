class Medida(object):
    def __init__(self, id=None, medida=None):
        self.id = id
        self.medida = medida

    def crear(self, nombre):
        query = "INSERT INTO unidad_medida (medida) VALUES (%s)"
        parametro = (nombre,)
        return query, parametro
    
    def modificar(self, nombre, id):
        query = "UPDATE unidad_medida SET medida=%s WHERE id_medida = %s"
        parametro = (nombre, id)
        return query, parametro

    def listar(self):
        return "SELECT * FROM unidad_medida"
    
    def obtener_uno(self, id):
        query = "SELECT * FROM unidad_medida WHERE id_medida = %s"
        parametro = (id,)
        return query, parametro