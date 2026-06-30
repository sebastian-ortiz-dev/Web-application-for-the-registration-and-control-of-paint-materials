from datetime import date, timedelta
from utils.obtener_fecha import mes
from utils.obtener_fecha import este_mes
class Tipo_listado(object):
    def __init__(self):
        pass

    def listar(self, id_categoria):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND p.id_categoria = %s" 
        parametros = (id_categoria,)
        return query, parametros
    
    def listar_no_movimientos(self, id_categoria):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.last_moviment = TRUE AND p.borrado = FALSE AND p.id_categoria = %s"
        parametros = (id_categoria,)
        return query, parametros
    
    def listar_minimo(self, id_categoria):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND p.cantidad <= p.cantidad_minima AND p.id_categoria = %s"
        parametros = (id_categoria,)
        return query, parametros

    def lista_proveedor(self, id_categoria):
        if id_categoria == 1:
            query = "SELECT * FROM distribuidor WHERE borrado = FALSE ORDER BY id_distribuidor DESC"
        elif id_categoria == 2:
            query = "SELECT * FROM distribuidor WHERE borrado = FALSE ORDER BY nombre ASC"
        elif id_categoria == 3:
            query = "SELECT * FROM distribuidor WHERE borrado = FALSE ORDER BY nombre DESC"
        elif id_categoria == 4:
            query = "SELECT * FROM distribuidor WHERE borrado = FALSE ORDER BY fecha_registro ASC"
        else:
            query = "SELECT * FROM distribuidor WHERE borrado = FALSE ORDER BY fecha_registro DESC"
        return query 
    
    def lista_usuario_filtro(self, id_categoria):
        if id_categoria == 1:
            query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario u INNER JOIN niveles_acceso n ON u.id_nivel =  n.id_nivel WHERE u.id_nivel = 1 AND u.borrado = FALSE"
        elif id_categoria == 2:
            query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario u INNER JOIN niveles_acceso n ON u.id_nivel =  n.id_nivel WHERE u.id_nivel = 2 AND u.borrado = FALSE"
        elif id_categoria == 3:
            query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario u INNER JOIN niveles_acceso n ON u.id_nivel =  n.id_nivel WHERE u.borrado = FALSE ORDER BY u.fecha_creacion ASC"
        else:
            query = "SELECT u.id_usuario, u.nombre_usuario, u.imagen_usu, n.nombre_nivel FROM usuario u INNER JOIN niveles_acceso n ON u.id_nivel =  n.id_nivel WHERE u.borrado = FALSE ORDER BY u.fecha_creacion DESC"
        return query 
    
    def lista_historial_filtro(self, id_categoria):
        if id_categoria == 5:
            query = "SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo, p.nombre_producto, u.nombre_usuario, mo.movimiento FROM public.movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto INNER JOIN usuario u ON m.id_usuario=u.id_usuario INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE cast(fecha as date) BETWEEN %s AND %s ORDER BY id_movimiento DESC"
            parametros = (date.today() - timedelta(days=7), date.today())

        elif id_categoria == 6:
            query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                        p.nombre_producto, u.nombre_usuario, mo.movimiento
                        FROM public.movimientos_inventario m 
                        INNER JOIN producto p ON m.id_producto=p.id_producto 
                        INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                        INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE cast(fecha as date) >= %s AND cast(fecha as date) < %s 
                        ORDER BY id_movimiento DESC"""
            parametros = (este_mes(date.today()), mes(date.today()))

        else:
            query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                        p.nombre_producto, u.nombre_usuario, mo.movimiento
                        FROM public.movimientos_inventario m 
                        INNER JOIN producto p ON m.id_producto=p.id_producto 
                        INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                        INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE m.tipo_movimiento = %s AND cast(fecha as date) = %s
                        ORDER BY id_movimiento DESC"""
            parametros = (id_categoria, date.today())
        return query, parametros