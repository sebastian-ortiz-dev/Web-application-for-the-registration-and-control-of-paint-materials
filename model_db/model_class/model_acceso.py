class Acceso(object):
    def __init__(self, id=None, nombre=None):
        self.id = id
        self.nombre = nombre
    
    def listar(self):
        return "SELECT * FROM niveles_acceso"
        


