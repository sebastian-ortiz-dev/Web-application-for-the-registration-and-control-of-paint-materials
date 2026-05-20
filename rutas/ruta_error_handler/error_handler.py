from flask import Blueprint, render_template, jsonify
from middleware.auth import *

handler_error_route = Blueprint('error_handler', __name__, template_folder='templates')

@handler_error_route.errorhandler(403)
@validation_jwt
def resource_not_found(datos_usuario, e):
    error = {'error_code': 404, 'message': "The resourse doesn't exist"}
    render_template('error_universal.html', status_code=403, error_title="Forbidden", error_message="Access to this resource on the server is denied."), 403
