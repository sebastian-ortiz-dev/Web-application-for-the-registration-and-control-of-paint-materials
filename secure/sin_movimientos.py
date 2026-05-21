from datetime import date, timedelta

def dia():
    hoy = date.today()
    hace_30 = hoy - timedelta(days=30)
    return hoy, hace_30

def sin_movimiento(id_productos, id_movimientos):
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

