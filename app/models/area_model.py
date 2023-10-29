from app.models import BaseModel
from sqlalchemy import Column, Integer, VARCHAR, SmallInteger


class AreaModel(BaseModel):
    __tablename__ = "areas"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    floor = Column(SmallInteger, nullable=False)
