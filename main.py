from app import application, db
from app import routers
from app.models import BaseModel


BaseModel.set_session(db.session)
