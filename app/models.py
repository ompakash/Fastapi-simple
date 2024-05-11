from .database import Base
from sqlalchemy import String,Integer,Boolean, Column
from sqlalchemy.sql.expression import null

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=True)
    