from datetime import date, timedelta
from utils.obtener_fecha import mes
from utils.obtener_fecha import este_mes

class Historia_Movimientos(object):
    def __init__(self):
        pass

    def movimiento(self, id_producto, cantidad, fecha, id_usuario, motivo, tipo_movimiento):
        query = "INSERT INTO movimientos_inventario (id_producto, cantidad, fecha, id_usuario, motivo, tipo_movimiento) VALUES (%s, %s, %s, %s, %s, %s)"
        parametros = (id_producto, cantidad, fecha, id_usuario, motivo, tipo_movimiento)
        return query, parametros

    def listar(self):
        query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                        p.nombre_producto, u.nombre_usuario, mo.movimiento
                        FROM public.movimientos_inventario m 
                        INNER JOIN producto p ON m.id_producto=p.id_producto 
                        INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                        INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE CAST(m.fecha as date) = %s
                        ORDER BY id_movimiento DESC""" 
        parametros = (date.today(),)
        return query, parametros
    
    def listar_intervalos(self, desde, hasta):
        query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                        p.nombre_producto, u.nombre_usuario, mo.movimiento
                        FROM public.movimientos_inventario m 
                        INNER JOIN producto p ON m.id_producto=p.id_producto 
                        INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                        INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE cast(fecha as date) BETWEEN %s AND %s
                        ORDER BY id_movimiento DESC"""
        parametros = (desde, hasta)
        return query, parametros
    
    def listar_hace_30(self, hoy, hace_30):
        query = "SELECT array_agg(DISTINCT m.id_producto) FROM public.movimientos_inventario as m INNER JOIN public.producto as p ON m.id_producto = p.id_producto WHERE CAST(m.fecha as date) >= %s AND CAST(m.fecha as date) <= %s AND p.borrado = FALSE" 
        parametros = (hace_30, hoy)
        #"SELECT array_agg(DISTINCT m.id_producto) FROM public.movimientos_inventario as m INNER JOIN public.producto as p ON m.id_producto = p.id_producto WHERE CAST(m.fecha as date) >= %s AND CAST(m.fecha as date) <= %s AND p.borrado = FALSE" 
        return query, parametros
    
    def lista_historial_filtro_intervalo(self, categoria, desde, hasta):
        query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                        p.nombre_producto, u.nombre_usuario, mo.movimiento
                        FROM public.movimientos_inventario m 
                        INNER JOIN producto p ON m.id_producto=p.id_producto 
                        INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                        INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE m.tipo_movimiento = %s AND CAST(m.fecha as date) BETWEEN %s AND %s 
                        ORDER BY id_movimiento DESC""" 
        parametros = (categoria, desde, hasta)
        return query, parametros
    
    def contar_devoluciones(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 3 AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = (este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_devoluciones_total_bs(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 3 AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = (este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_entradas(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 1 AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = (este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_entradas_total_bs(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 1 AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = (este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_salidas(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 2 AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = (este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_salidas_total_bs(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 2 AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = (este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_ajustes(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 4 AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = (este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_ajustes_total_aumento(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 4 AND motivo = %s AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = ('Error de conteo, aumento de stock', este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_ajustes_total_disminucion(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 4 AND motivo = %s AND CAST(fecha as date) BETWEEN %s AND %s" 
        parametros = ('Error de conteo, disminucion de stock', este_mes(date.today()), mes(date.today()))
        return query, parametros
    
    def contar_devoluciones_hoy(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 3 AND CAST(fecha as date) = %s" 
        parametros = (date.today(),)
        return query, parametros
    
    def contar_devoluciones_total_bs_hoy(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 3 AND CAST(fecha as date) = %s" 
        parametros = (date.today(),)
        return query, parametros
    
    def contar_entradas_hoy(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 1 AND CAST(fecha as date) = %s" 
        parametros = (date.today(),)
        return query, parametros
    
    def contar_entradas_total_bs_hoy(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 1 AND CAST(fecha as date) = %s" 
        parametros = (date.today(),)
        return query, parametros
    
    def contar_salidas_hoy(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 2 AND CAST(fecha as date) = %s" 
        parametros = (date.today(),)
        return query, parametros
    
    def contar_salidas_total_bs_hoy(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 2 AND CAST(fecha as date) = %s" 
        parametros = (date.today(),)
        return query, parametros
    
    def contar_ajustes_hoy(self):
        query = "SELECT COUNT(id_movimiento) FROM movimientos_inventario WHERE tipo_movimiento = 4 AND CAST(fecha as date) = %s" 
        parametros = (date.today(),)
        return query, parametros
    
    def contar_ajustes_total_aumento_hoy(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 4 AND motivo = %s AND CAST(fecha as date) = %s" 
        parametros = ('Error de conteo, aumento de stock', date.today())
        return query, parametros
    
    def contar_ajustes_total_disminucion_hoy(self):
        query = "SELECT COALESCE(SUM(m.cantidad * p.precio_venta), 0.00) FROM movimientos_inventario m INNER JOIN producto p ON m.id_producto=p.id_producto WHERE tipo_movimiento = 4 AND motivo = %s AND CAST(fecha as date) = %s" 
        parametros = ('Error de conteo, disminucion de stock', date.today())
        return query, parametros

    def busqueda_historial(self, filtro):
        query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                        p.nombre_producto, u.nombre_usuario, mo.movimiento
                        FROM public.movimientos_inventario m 
                        INNER JOIN producto p ON m.id_producto=p.id_producto 
                        INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                        INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE CAST(m.fecha as date) = %(fecha)s AND 
                        (m.motivo ILIKE %(busqueda)s OR m.id_movimiento::text ILIKE %(busqueda)s OR p.nombre_producto ILIKE %(busqueda)s 
                        OR u.nombre_usuario ILIKE %(busqueda)s OR m.id_producto::text ILIKE %(busqueda)s) ORDER BY m.id_movimiento DESC"""
                        
        parametros = {'busqueda': filtro, 'fecha': date.today()}
        return query, parametros
    
    def busqueda_historial_filtrado_dias(self, filtro, categoria):
        if categoria == 5:
            query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                            p.nombre_producto, u.nombre_usuario, mo.movimiento
                            FROM public.movimientos_inventario m 
                            INNER JOIN producto p ON m.id_producto=p.id_producto 
                            INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                            INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE CAST(m.fecha as date) BETWEEN %(siete_dias)s AND %(hoy)s 
                            AND (m.motivo ILIKE %(busqueda)s OR m.id_movimiento::text ILIKE %(busqueda)s OR p.nombre_producto ILIKE %(busqueda)s 
                            OR u.nombre_usuario ILIKE %(busqueda)s OR m.id_producto::text ILIKE %(busqueda)s) 
                            ORDER BY m.id_movimiento DESC """
            parametros = {'busqueda': filtro, 'siete_dias': date.today() - timedelta(days=7), 'hoy': date.today()}
            
        elif categoria == 6:
            query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                                p.nombre_producto, u.nombre_usuario, mo.movimiento
                                FROM public.movimientos_inventario m 
                                INNER JOIN producto p ON m.id_producto=p.id_producto 
                                INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                                INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE cast(fecha as date) >= %(mes)s AND cast(fecha as date) < %(siguiente)s
                                AND (m.motivo ILIKE %(busqueda)s OR m.id_movimiento::text ILIKE %(busqueda)s OR p.nombre_producto ILIKE %(busqueda)s 
                                OR u.nombre_usuario ILIKE %(busqueda)s OR m.id_producto::text ILIKE %(busqueda)s) 
                                ORDER BY m.id_movimiento DESC """
            parametros = {'busqueda': filtro, 'siguiente': mes(date.today()), 'mes': este_mes(date.today())}
            
        else:
            query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                            p.nombre_producto, u.nombre_usuario, mo.movimiento
                            FROM public.movimientos_inventario m 
                            INNER JOIN producto p ON m.id_producto=p.id_producto 
                            INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                            INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE m.tipo_movimiento = %(tipo)s AND cast(fecha as date) = %(fecha)s
                            AND (m.motivo ILIKE %(busqueda)s OR m.id_movimiento::text ILIKE %(busqueda)s OR p.nombre_producto ILIKE %(busqueda)s 
                            OR u.nombre_usuario ILIKE %(busqueda)s OR m.id_producto::text ILIKE %(busqueda)s) 
                            ORDER BY m.id_movimiento DESC """
            parametros = {'busqueda': filtro, 'tipo': categoria, 'fecha': date.today()}
             
        return query, parametros    
    
    
    def busqueda_historial_intervalos(self, filtro, desde, hasta):
        query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                    p.nombre_producto, u.nombre_usuario, mo.movimiento
                    FROM public.movimientos_inventario m 
                    INNER JOIN producto p ON m.id_producto=p.id_producto 
                    INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                    INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE CAST(m.fecha as date) BETWEEN %(desde)s AND %(hasta)s 
                    AND (m.motivo ILIKE %(busqueda)s OR m.id_movimiento::text ILIKE %(busqueda)s OR p.nombre_producto ILIKE %(busqueda)s 
                    OR u.nombre_usuario ILIKE %(busqueda)s OR m.id_producto::text ILIKE %(busqueda)s) 
                    ORDER BY m.id_movimiento DESC """
        parametros = {'busqueda': filtro, 'desde': desde, 'hasta': hasta}
        return query, parametros
    
    def busqueda_historial_intervalos_Categoria(self, filtro, desde, hasta, categoria):
        query = """SELECT m.id_movimiento, m.id_producto, m.cantidad, m.fecha, m.id_usuario, m.motivo,  
                    p.nombre_producto, u.nombre_usuario, mo.movimiento
                    FROM public.movimientos_inventario m 
                    INNER JOIN producto p ON m.id_producto=p.id_producto 
                    INNER JOIN usuario u ON m.id_usuario=u.id_usuario
                    INNER JOIN movimientos mo ON m.tipo_movimiento=mo.id WHERE  m.tipo_movimiento = %(categoria)s AND CAST(m.fecha as date) BETWEEN %(desde)s AND %(hasta)s 
                    AND (m.motivo ILIKE %(busqueda)s OR m.id_movimiento::text ILIKE %(busqueda)s OR p.nombre_producto ILIKE %(busqueda)s 
                    OR u.nombre_usuario ILIKE %(busqueda)s OR m.id_producto::text ILIKE %(busqueda)s) 
                    ORDER BY m.id_movimiento DESC """
        parametros = {'busqueda': filtro, 'desde': desde, 'hasta': hasta, 'categoria':categoria}
        return query, parametros