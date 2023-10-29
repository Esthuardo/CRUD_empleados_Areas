from flask_restx import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.area_model import AreaModel


class AreaRequestSchema:
    def __init__(self, namespace):
        self.ns = namespace

    def create(self):
        return self.ns.model(
            "Area Create",
            {
                "name": fields.String(required=True, max_length=50),
                "floor": fields.Integer(required=True),
            },
        )

    def update(self):
        return self.ns.model(
            "Area Update",
            {
                "name": fields.String(required=True, max_length=50),
                "floor": fields.Integer(required=True),
            },
        )


class AreaResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AreaModel
