from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Memes(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    src = Column(String(255), nullable=True)
    description = Column(String(200), nullable=True)
