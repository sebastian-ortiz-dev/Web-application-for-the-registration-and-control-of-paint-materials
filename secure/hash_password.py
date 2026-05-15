from argon2 import PasswordHasher

ph = PasswordHasher()
class Hash_password(object):
    def __init__(self):
        pass

    def hash_password_verify(self, hash_db, password):
        try:
            ph.verify(hash_db, password)
            if ph.check_needs_rehash(hash_db):
                new_hash = self.rehash(password)
                return new_hash
        except Exception as e:
            print(f"incorrect password: {e}")
            return False

    def create_hash(self, password):
        hash = ph.hash(password)
        return hash            

    def rehash(self, password):
        new_hash = ph.hash(password)
        return new_hash