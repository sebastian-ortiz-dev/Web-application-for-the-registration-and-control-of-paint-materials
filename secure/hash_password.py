from argon2 import PasswordHasher

ph = PasswordHasher()
class Hash_password(object):
    def __init__(self):
        pass

    def hash_password_verify(self, hash_db, password, recuperado, usuarios, instancia_conexion, cursor, pool_db):
        try:
            ph.verify(hash_db, password)
            if ph.check_needs_rehash(hash_db):
                self.rehash(password, recuperado, usuarios, instancia_conexion, cursor, pool_db)
            return True
        except Exception as e:
            print(f"incorrect password: {e}")
            return False

    def create_hash(self, password):
        hash = ph.hash(password)
        return hash            

    def rehash(self, password, recuperado, usuarios, instancia_conexion, cursor, pool_db):
        new_hash = ph.hash(password)
        text, parameters = usuarios.user_rehash(new_hash, recuperado)
        instancia_conexion.registrar(cursor, text, parameters)
        instancia_conexion.ejecutar_cambio(pool_db)