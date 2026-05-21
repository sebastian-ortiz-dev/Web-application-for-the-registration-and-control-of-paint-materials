from model_db.model_class.model_acceso import Acceso
from model_db.model_class.model_categoria import Categoria
from model_db.model_class.model_historial import Historia_Movimientos
from model_db.model_class.model_listado import Tipo_listado
from model_db.model_class.model_medida import Medida
from model_db.model_class.model_movimientos import Movimientos
from model_db.model_class.model_producto import Producto
from model_db.model_class.model_proveedor import Proveedor
from model_db.model_class.model_usuario import Usuario
from model_db.model_class.model_refresh_token import Refresh_token
from secure.hash_password import Hash_password
from model_db.conexion import Conexion

instancia_conexion = Conexion()
usuarios = Usuario()
refresh = Refresh_token()
hash = Hash_password()
productor = Producto()
medida = Medida()
category = Categoria()
historial = Historia_Movimientos()
proveedor = Proveedor()
listado = Tipo_listado()
movimientos = Movimientos()
acceso = Acceso()