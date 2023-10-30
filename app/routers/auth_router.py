from app import api
from flask_restx import Resource
from flask import request
from app.schemas.auth_schema import AuthRequestSchema
from app.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_ns = api.namespace(
    name="Authentication", description="Rutas del módulo de autenticación", path="/auth"
)
schema_request = AuthRequestSchema(auth_ns)
controller = AuthController()


@auth_ns.route("/signin")
class Sigin(Resource):
    @auth_ns.expect(schema_request.login(), validation=True)
    def post(self):
        """Login de usuario"""
        return controller.sign_in(request.json)


@auth_ns.route("/token/refresh")
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @auth_ns.expect(schema_request.refresh(), validation=True)
    def post(self):
        """Obtener un nuevo access_token si este a vencido"""
        identity = get_jwt_identity()
        return controller.refresh_token(identity)


@auth_ns.route("/password/reset")
class PasswordReset(Resource):
    @auth_ns.expect(schema_request.reset(), validate=True)
    def post(self):
        """Generar nueva contraseña de usuario"""
        return controller.password_reset(request.json)
