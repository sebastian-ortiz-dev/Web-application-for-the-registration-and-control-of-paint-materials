class Producto(object):
    def __init__(self):
        pass

    def create_producto(self, nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, id_categoria, id_medida, minimo):
        query = "INSERT INTO producto (nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, borrado, id_categoria, id_medida, cantidad_minima) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        parametros = (nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, 'false', id_categoria, id_medida, minimo)    
        return query, parametros
        
    def modificar_producto(self, id, nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, id_categoria, minima, id_medida):
        query = "UPDATE producto SET nombre_producto= %s, descripcion= %s, precio_venta= %s, cantidad= %s, fecha_actualizacion= %s, imagen= %s, id_distribuidor= %s, id_categoria= %s, id_medida= %s, cantidad_minima=%s WHERE id_producto = %s"
        parametros = (nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, id_categoria, id_medida, minima, id)
        return query, parametros

    def modifica_cantidad(self, id, cantidad_total):
        query = "UPDATE producto SET cantidad= %s, last_moviment= FALSE WHERE id_producto = %s" 
        parametros = (cantidad_total, id)
        return query, parametros

    def modificar_cantidad_sin_movimientos(self, lista):
        query = "UPDATE producto SET last_moviment= %s WHERE id_producto IN %s AND borrado = FALSE"
        parametros = ("TRUE", lista)        
        return query, parametros

    def contar_productos_inactivo(self):
        return "SELECT COALESCE(COUNT(id_producto), 0) FROM producto WHERE borrado = TRUE"

    def eliminar_producto(self, id):
        query = "UPDATE producto SET borrado=%s WHERE id_producto = %s"
        parametros = ("TRUE", id)        
        return query, parametros
    
    def recuperar_producto(self, id):
        query = "UPDATE producto SET borrado=%s WHERE id_producto = %s"
        parametros = ("FALSE", id)        
        return query, parametros

    def listar(self):
        return "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE ORDER BY p.id_producto ASC"
    
    def listar_inactivo(self):
        return "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = TRUE"
    
    def listar_minimo(self):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND p.cantidad <= p.cantidad_minima"
        return query
    
    def listar_minimo_cantidad(self):
        query = "SELECT COALESCE(COUNT(cantidad), 0) FROM producto WHERE borrado = FALSE AND cantidad <= cantidad_minima"
        return query
    
    def listar_necesario(self):
        return "SELECT producto.id_producto, producto.nombre_producto FROM producto WHERE borrado=false ORDER BY producto.id_producto ASC"
    
    def listar_lista(self, lista):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.id_producto IN %s AND p.borrado = FALSE ORDER BY p.id_producto ASC "
        parametros = (lista,)
        return query, parametros
    
    def listar_id(self):
        return "SELECT array_agg(producto.id_producto) FROM producto WHERE borrado = FALSE AND producto.last_moviment = FALSE" 

    def listar_id_unicos(self, lista):
        query = "SELECT producto.id_producto FROM producto WHERE id_producto IN %s AND borrado = FALSE"
        parametros = (lista,)
        return query, parametros
    
    def listar_sin_movimiento(self):
        return "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.last_moviment = TRUE AND p.borrado = FALSE"

    def obtener_cantidad_sin_movimientos(self):
        return "SELECT COALESCE(COUNT(producto.id_producto), 0) FROM producto WHERE last_moviment = TRUE AND borrado = FALSE"
    
    def cantidad_sin_movimientos_bs(self):
        return "SELECT COALESCE(sum(producto.id_producto * producto.cantidad), 0.00) FROM producto WHERE last_moviment = TRUE AND borrado = FALSE"

    def obtener_uno(self, id):
        query = "SELECT p.id_producto, p.nombre_producto, p.descripcion, p.precio_venta, p.cantidad, p.imagen, p.cantidad_minima, p.fecha_actualizacion, c.categoria, um.medida, d.id_distribuidor, d.nombre FROM producto p INNER JOIN distribuidor d ON p.id_distribuidor = d.id_distribuidor INNER JOIN categorias c ON p.id_categoria = c.id_categoria INNER JOIN unidad_medida um ON p.id_medida = um.id_medida WHERE p.id_producto=%s"
        parametros = (id,)        
        return query, parametros

    def obtene_por_nombre(self, nombre, descripcion, precio, cantidad, minimo):
        query = "SELECT id_producto FROM producto WHERE borrado = false AND nombre_producto=%s AND descripcion=%s AND precio_venta=%s AND cantidad=%s AND cantidad_minima=%s"
        parametros = (nombre, descripcion, precio, cantidad, minimo)        
        return query, parametros
    
    def obtener_distribuidores(self):
        return "SELECT DISTINCT(id_distribuidor) FROM producto WHERE borrado = false"
    
    def obtener_proveedores(self, id):
        query = "SELECT DISTINCT(id_distribuidor) FROM producto WHERE id_producto in %s"
        parametros = (id,)        
        return query, parametros

    def obtener_cantidad(self, id):
        query = "SELECT cantidad FROM producto WHERE id_producto=%s FOR UPDATE"
        parametros = (id,)        
        return query, parametros
    
    def obtener_cantidad_productos(self):
        return "SELECT SUM(precio_venta * cantidad) FROM producto WHERE borrado = FALSE"
    
    def busqueda_productos(self, filtro):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND (p.nombre_producto ILIKE %(busqueda)s OR p.id_producto::text ILIKE %(busqueda)s OR p.id_distribuidor::text ILIKE %(busqueda)s OR p.id_categoria::text ILIKE %(busqueda)s) ORDER BY p.id_producto ASC"
        parametros = {'busqueda': filtro}        
        return query, parametros
    
    def busqueda_productos_inactivo(self, filtro):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = TRUE AND (p.nombre_producto ILIKE %(busqueda)s OR p.id_producto::text ILIKE %(busqueda)s OR p.id_distribuidor::text ILIKE %(busqueda)s OR p.id_categoria::text ILIKE %(busqueda)s) ORDER BY p.id_producto ASC"
        parametros = {'busqueda': filtro}        
        return query, parametros
    
    def busqueda_productos_categoria(self, filtro, categoria):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND p.id_categoria = %(categoria)s AND (p.nombre_producto ILIKE %(busqueda)s OR p.id_producto::text ILIKE %(busqueda)s OR p.id_distribuidor::text ILIKE %(busqueda)s OR p.id_categoria::text ILIKE %(busqueda)s) ORDER BY p.id_producto ASC"
        parametros = {'busqueda': filtro, 'categoria': categoria}      
        return query, parametros
    
    def busqueda_productos_minimo(self, filtro):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND (p.nombre_producto ILIKE %(busqueda)s OR p.id_producto::text ILIKE %(busqueda)s OR p.id_distribuidor::text ILIKE %(busqueda)s OR p.id_categoria::text ILIKE %(busqueda)s) AND p.cantidad <= p.cantidad_minima ORDER BY p.id_producto ASC" 
        parametros = {'busqueda': filtro}     
        return query, parametros
    
    def busqueda_minimo_categoria(self, filtro, categoria):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND p.id_categoria = %(categoria)s AND p.cantidad <= p.cantidad_minima AND (p.nombre_producto ILIKE %(busqueda)s OR p.id_producto::text ILIKE %(busqueda)s OR p.id_distribuidor::text ILIKE %(busqueda)s OR p.id_categoria::text ILIKE %(busqueda)s) ORDER BY p.id_producto ASC" 
        parametros = {'busqueda': filtro, 'categoria': categoria}    
        return query, parametros
    
    def busqueda_productos_sin_movimiento(self, filtro):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND p.last_moviment = TRUE AND (p.nombre_producto ILIKE %(busqueda)s OR p.id_producto::text ILIKE %(busqueda)s OR p.id_distribuidor::text ILIKE %(busqueda)s OR p.id_categoria::text ILIKE %(busqueda)s) ORDER BY p.id_producto ASC"
        parametros = {'busqueda': filtro}     
        return query, parametros
    
    def busqueda_productos_categoria_sin_movimientos(self, filtro, categoria):
        query = "SELECT p.id_producto, p.nombre_producto, p.id_distribuidor, p.cantidad, p.imagen, p.precio_venta, p.id_categoria, u.medida FROM producto p INNER JOIN unidad_medida u ON p.id_medida = u.id_medida WHERE p.borrado = FALSE AND p.id_categoria = %(categoria)s AND p.last_moviment = TRUE AND (p.nombre_producto ILIKE %(busqueda)s OR p.id_producto::text ILIKE %(busqueda)s OR p.id_distribuidor::text ILIKE %(busqueda)s OR p.id_categoria::text ILIKE %(busqueda)s) ORDER BY p.id_producto ASC" 
        parametros = {'busqueda': filtro, 'categoria': categoria}     
        return query, parametros