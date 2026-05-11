def este_mes(fecha):
    day = 1
    year = fecha.year
    month = fecha.month
    if month < 10:
        dia = (f'{year}-0{month}-0{day}') 
    else:
        dia = (f'{year}-{month}-0{day}') 
    return dia

def mes(fecha):
    day = 1
    year = fecha.year

    if fecha.month != 12:        
        month = fecha.month + 1
    else:
        year = fecha.year + 1
        month = 1

    if month < 10:
        dia = (f'{year}-0{month}-0{day}') 
    else:
        dia = (f'{year}-{month}-0{day}') 

    return dia
