from app import db, mail
from app.models.employee_model import EmployeeModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token
from secrets import token_hex
from app.utils.mailing import Mailing
from os import getenv


class AuthController:
    def __init__(self):
        self.db = db
        self.model = EmployeeModel
        self.mailing = Mailing()

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

    def password_reset(self, body):
        try:
            email = body["email"]
            record = self.model.where(email=email).first()
            if record:
                new_password = token_hex(6)
                record.password = new_password
                record.hash_password()
                self.db.session.add(record)
                self.db.session.commit()
                self.mailing.email_reset_password(email, record.name, new_password)
                return {
                    "message": "Se envio un correo con la nueva contraseña",
                }, HTTPStatus.OK
            else:
                return {
                    "message": f"No se encontro un usuario con el correo: {email}",
                }, HTTPStatus.NOT_FOUND
        except Exception as e:
            self.db.session.rollback()
            return {
                "message": "Ocurrio un error",
                "error": str(e),
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()
