from app.models import BaseModel
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, String
from bcrypt import hashpw, gensalt, checkpw


class EmployeeModel(BaseModel):
    __tablename__ = "employee"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    surname = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    password = Column(String(255))
    area_id = Column(Integer, ForeignKey("areas.id"))

    def hash_password(self):
        password_encode = self.password.encode("utf-8")
        password_hash = hashpw(password_encode, gensalt(rounds=10))
        self.password = password_hash.decode("utf-8")

    def check_password(self, password):
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
