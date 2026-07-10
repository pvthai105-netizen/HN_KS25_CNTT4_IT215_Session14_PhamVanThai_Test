from database import Base
from sqlalchemy import Column, Integer, String



class teams(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(30), nullable=False)
    coach_name = Column(String(50), nullable=False)
    group_name = Column(String(50), nullable=False)
    points = Column(Integer, nullable=False)

    