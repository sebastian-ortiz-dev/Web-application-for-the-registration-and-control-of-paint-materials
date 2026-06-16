from model_db.class_singlen import instancia_conexion, usuarios

def test_get_all_customers():
    pool, cursor = instancia_conexion.iniciar_conexion()
    user = usuarios.listar()
    come_back = instancia_conexion.todos(cursor, user)
    instancia_conexion.cerrar_conexion(cursor, pool)
    assert len(come_back) == 1