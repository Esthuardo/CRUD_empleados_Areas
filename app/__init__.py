from os import getenv
from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import environment
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
FLASK_ENV = getenv("FLASK_ENV")
ENVIRONMENT = environment[FLASK_ENV]
app.config.from_object(ENVIRONMENT)

authorization = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    app,
    title="Empleados Api",
    version="0.1",
    description="Tarea CRUD de empleados",
    doc="/swagger-ui",
    authorizations=authorization,
)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)

mail = Mail(app)
