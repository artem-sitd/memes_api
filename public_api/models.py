from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Memes(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    src = Column(String(255), nullable=True, unique=True)
    description = Column(String(200), nullable=True, unique=True)

    __table_args__ = (
        UniqueConstraint('src', 'description', name='_src_description_uc'),
    )
