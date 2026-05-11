def get_producto_id(productos):
    id_productos = []
    for id in range(len(productos)):
        indice = productos[id][0]
        id_productos.append(indice)
    return id_productos