from app import api
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from app.controllers.areas_controller import AreaController
from app.schemas.areas_schema import AreaRequestSchema

area_ns = api.namespace(
    name="Areas", description="Rutas del modulo Areas", path="/areas"
)
schema_request = AreaRequestSchema(area_ns)
controller = AreaController()


# CRUD
@area_ns.route("")
@area_ns.doc(security="Bearer")
class Areas(Resource):
    # dispatch
    @jwt_required()
    def get(self):
        """Listar todos los Areas"""
        return controller.fetch_all()

    @area_ns.expect(schema_request.create(), validate=True)
    @jwt_required()
    def post(self):
        """Creación de un rol"""
        return controller.save(request.json)


@area_ns.route("/<int:id>")
@area_ns.doc(security="Bearer")
class AreaById(Resource):
    def get(self, id):
        """Encontrar un área por su ID"""
        return controller.find_by_id(id)

    @jwt_required()
    def patch(self, id):
        """Actualizar un área por su ID"""
        return controller.update(id, request.json)

    @jwt_required()
    def delete(self, id):
        """Eliminar un área por su ID"""
        return controller.remove(id)
