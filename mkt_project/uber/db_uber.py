from datetime import datetime
from pathlib import Path
from random import randint

from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import Session, declarative_base, relationship

engine = create_engine("postgresql+psycopg2://biba:Ubuntu11!!@localhost/mkt_base")
session = Session(bind=engine)
BASE_DIR = Path(__file__).resolve().parent.parent

Base = declarative_base()

class CustomersUber(Base):
    __tablename__ = 'customers_uber'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_phone_mammoth = Column(Text, nullable=True)
    worker_id = Column(BigInteger, nullable=False)
    worker_username = Column(Text, nullable=False)
    from_address = Column(Text, default=None)
    to_address = Column(Text, default=None)
    num_id_order_fake = Column(Text, default=str(randint(1000000, 6800000)))
    price = Column(Text)
    card = Column(Text, nullable=True)
    bank = Column(Text, nullable=True)
    code = Column(Text, nullable=True)
    data = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    link = Column(Text, unique=True)

Base.metadata.create_all(engine)

