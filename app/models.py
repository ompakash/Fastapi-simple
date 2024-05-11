from .database import Base
from sqlalchemy import String,Integer,Boolean, Column
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE' ,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default= text('now()'),nullable=False)