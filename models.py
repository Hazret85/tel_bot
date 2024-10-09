import pytz
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URI = 'sqlite:///bot_logs.db'


engine = create_engine(DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
MSK = pytz.timezone('Europe/Moscow')

Base = declarative_base()


class BotLog(Base):
    __tablename__ = 'bot_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(String(255))
    command = Column(String(50))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=lambda: datetime.now(MSK))


Base.metadata.create_all(engine)
