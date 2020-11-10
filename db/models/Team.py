from sqlalchemy import Column, Integer, String
from db.Config import Base


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nationality = Column(String)

