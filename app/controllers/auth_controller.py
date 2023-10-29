from app import db
from app.models.employee_model import EmployeeModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token


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
                refresh_token = create_refresh_token(identity=user_id)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, HTTPStatus.OK
            else:
                return {
                    "message": f"La contraseña del usuario {email} es incorrecta",
                }, HTTPStatus.UNAUTHORIZED

        except Exception as e:
            return {
                "message": "Ocurrio un error",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def refresh_token(self, identity):
        try:
            access_token = create_access_token(identity=identity)
            return {
                "access_token": access_token,
            }, HTTPStatus.OK
        except Exception as e:
            return {
                "message": "Ocurrio un error",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
