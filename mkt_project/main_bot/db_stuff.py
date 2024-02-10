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

class User(Base):
    __tablename__ = 'user_bot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(Text, nullable=False, unique=True)
    status = Column(Integer, default=0)  # 0 - без оформленной заявки, 1 - воркер, 2 - тп, 3 - вбив, 4 - админ, 5 - тс
    data_join = Column(Date, default=datetime.now)
    category = Column(Text, default='Нету')

class Bids(Base):
    __tablename__ = 'bids'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    text = Column(Text, nullable=False)
    status = Column(Integer, default=0)  # 0 - не овтетили, 1 - разрешено, 2 - отказано

class Profits(Base):
    __tablename__ = 'profits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    username_worker = Column(Text)
    full_profit = Column(Float)
    percent = Column(Float, default=70.0)
    share_workers = Column(Float, default=None) # Часть воркера
    tech_supp_username = Column(Text, default='Нету')
    is_reffil = Column(Boolean, default=False)
    date = Column(Date, default=datetime.now)
    category = Column(Text)
    vbiv_username = Column(Text, default='Нету')

class Links(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    link = Column(Text, nullable=False)
    work = Column(Boolean, default=True)
    category = Column(Text, nullable=False)
    date = Column(Date, default=datetime.now)
    mammoths = Column(ARRAY(String(200)), default=[])
    from_address = Column(Text, default='Адрес пользователя скрыт')
    to_address = Column(Text, default='Куда?')
    num_id_order_fake = Column(Text, default=str(randint(1000000, 6800000)))
    price = Column(Text, default=None)

# class UberPreLinks(Base):
#     __tablename__ = 'uber_pre_links'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     price = Column(Text, nullable=True)
#     address_to = Column(Text, nullable=True)
#     address_from = Column(Text, nullable=True)

class About(Base):
    __tablename__ = 'about'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text)

class Cards(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(30), nullable=False)  # кз, укр, рус
    numbers = Column(Text, nullable=False)

class Domenes(Base):
    __tablename__ = 'domenes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(Text, nullable=False)
    work = Column(Boolean, default=True)
    category = Column(Text, nullable=False)

# def before_update_listener(mapper, connection, target):
#     if 'tech_supp_username' in target.__dict__ and target.tech_supp_username != 'Нету':
#         target.percent -= 5.0
#     if 'is_reffil' in target.__dict__ and target.is_reffil:
#         target.percent -= 10.0
#
#     target.share_workers = (target.full_profit / 100) * target.percent
#
# def arter_insert_listener(mapper, connection, target):
#     if 'tech_supp_username' in target.__dict__ and target.tech_supp_username != 'Нету':
#         target.percent -= 5.0
#
#     if 'is_reffil' in target.__dict__ and target.is_reffil:
#         target.percent -= 10.0
#
#     target.share_workers = (target.full_profit / 100) * target.percent
#
# event.listen(Profits, 'before_update', before_update_listener)
# event.listen(Profits, 'after_insert', arter_insert_listener)

Base.metadata.create_all(engine)




