from flask_restx import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.employee_model import EmployeeModel
from flask_restx.reqparse import RequestParser


class EmployeesRequestSchema:
    def __init__(self, namespace):
        self.ns = namespace

    def create(self):
        return self.ns.model(
            "Employee Create",
            {
                "name": fields.String(required=True, max_length=50),
                "surname": fields.String(required=True, max_length=50),
                "email": fields.String(required=True, max_length=80),
                "password": fields.String(required=True, max_length=18),
                "area_id": fields.Integer(required=True),
            },
        )

    def all(self):
        parser = RequestParser()
        parser.add_argument("page", type=int, default=1, location="args")
        parser.add_argument("per_page", type=int, default=5, location="args")
        parser.add_argument("email", type=str, location="args")
        parser.add_argument("name", type=str, location="args")
        return parser

    def update(self):
        return self.ns.model(
            "Employee Update",
            {
                "name": fields.String(required=False, max_length=50),
                "surname": fields.String(required=False, max_length=50),
                "email": fields.String(required=True, max_length=50),
                "area_id": fields.Integer(required=True),
            },
        )


class EmployeesResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeModel
        exclude = ["password"]
