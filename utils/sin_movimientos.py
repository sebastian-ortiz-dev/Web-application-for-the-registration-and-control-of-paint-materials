def sin_movimiento(id_productos, id_movimientos):
        if id_movimientos is None or id_productos is None:
            no_movimientos = []
        else:
            no_movimientos = set(id_productos) - set(id_movimientos)
        return no_movimientos

def limpiar(lista):
    limpio_id = []
    if len(lista) == 0:
        return []
    else:
        for i in range(len(lista)):
            limpio_id.append(lista[i][0])
    return limpio_id

