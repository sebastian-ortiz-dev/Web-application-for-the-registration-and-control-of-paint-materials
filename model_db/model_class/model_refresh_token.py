class Refresh_token(object):
    def __init__(self):
        pass
    
    def create_refresh(self, id_user, uuid, is_revoked, date):
        query = "INSERT INTO refresh_token (id_usuario, uuid, is_revoked, date_expired) VALUES (%s, %s, %s, %s)"
        parameters = (id_user, uuid, is_revoked, date)
        return query, parameters
    
    def update_refresh(self, uuid):
        query = "UPDATE refresh_token SET is_revoked=%s WHERE uuid=%s"
        parameters = (True, uuid)
        return query, parameters
    
    def verify_refresh(self, uuid, date):
        query = "SELECT id_usuario, uuid FROM refresh_token WHERE is_revoked=False AND uuid=%s AND %s <= date_expired"
        parametros = (uuid, date)
        return query, parametros
    
    def verify_refresh_login(self, id, date):
        query = "SELECT id_usuario, uuid FROM refresh_token WHERE is_revoked=False AND id_usuario=%s AND %s <= date_expired"
        parametros = (id, date)
        return query, parametros