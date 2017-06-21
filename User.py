from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine('mysql://root:maportofeup2014@mysqlserver/flask')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
