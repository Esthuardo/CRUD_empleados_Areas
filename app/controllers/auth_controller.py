from app import db
from app.models.employee_model import EmployeeModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token


class AuthController:
    def __init__(self):
        self.db = db
        self.model = EmployeeModel

    def sign_in(self, body):
        try:
            email = body["email"]
            password = body["password"]
            record = self.model.where(email=email).first()
            if record.check_password(password):
                user_id = record.id
                access_token = create_access_token(identity=user_id)
                return {"auth": access_token}, HTTPStatus.OK
            else:
                return {
                    "message": f"La contraseña del usuario {email} es incorrecta",
                }, HTTPStatus.UNAUTHORIZED

        except Exception as e:
            return {
                "message": "Ocurrio un error",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
