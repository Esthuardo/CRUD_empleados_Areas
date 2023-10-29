from app import api
from flask_restx import Resource
from flask import request
from app.schemas.auth_schema import AuthRequestSchema
from app.controllers.auth_controller import AuthController

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
