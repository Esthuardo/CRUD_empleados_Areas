from app import api
from flask import request
from flask_restx import Resource
from app.controllers.employees_controller import EmployeesController
from app.schemas.employees_schema import EmployeesRequestSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

employee_ns = api.namespace(
    name="Empleados", description="Rutas del modulo Empleados", path="/empleados"
)
schema_request = EmployeesRequestSchema(employee_ns)
controller = EmployeesController()


# CRUD
@employee_ns.route("")
@employee_ns.doc(security="Bearer")
class Employee(Resource):
    # dispatch
    @employee_ns.expect(schema_request.all())
    @jwt_required()
    def get(self):
        """Listar todos los empleados"""
        email = request.args.get("email")
        name = request.args.get("name")
        return controller.fetch_all(email=email, name=name)

    @employee_ns.expect(schema_request.create(), validate=True)
    @jwt_required()
    def post(self):
        """Creación de un rol"""
        return controller.save(request.json)


@employee_ns.route("/<int:id>")
@employee_ns.doc(security="Bearer")
class EmployeeById(Resource):
    @jwt_required()
    def patch(self, id):
        """Actualizar un empleado por su ID"""
        return controller.update(id, request.json)

    @jwt_required()
    def delete(self, id):
        """Eliminar un empleado por su ID"""
        return controller.remove(id)


@employee_ns.route("/profile/me")
@employee_ns.doc(security="Bearer")
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """Obtener los datos del usuario conectado"""
        identity = get_jwt_identity()
        return controller.profile_me(identity)
