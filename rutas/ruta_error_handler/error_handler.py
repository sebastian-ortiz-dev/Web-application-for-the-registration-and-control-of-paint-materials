from flask import Blueprint, render_template
from middleware.auth import validation_jwt

handler_error_route = Blueprint('error_handler', __name__, template_folder='templates')

@handler_error_route.app_errorhandler(403)
@validation_jwt
def forbidden(datos_usuario, e):
    return render_template('error_universal.html', status_code=403, error_title="Forbidden", error_message="Access to this resource on the server is denied."), 403

@handler_error_route.app_errorhandler(404)
@validation_jwt
def resource_not_found(datos_usuario, e):
    return render_template('error_universal.html', status_code=404, error_title="Resource not found", error_message="Verify the URL"), 404

@handler_error_route.app_errorhandler(405)
@validation_jwt
def resource_not_found(datos_usuario, e):
    return render_template('error_universal.html', status_code=405, error_title="Method not allowed", error_message="The method http isn't allow in this endpoint"), 405

@handler_error_route.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error_universal.html', status_code=500, error_title="Internal Server Error", error_message="Something went wrong. Please try again later."), 500
