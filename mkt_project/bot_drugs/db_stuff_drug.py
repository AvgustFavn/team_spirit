from datetime import datetime
from pathlib import Path

from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import Session, declarative_base, relationship

engine = create_engine("postgresql+psycopg2://biba:Ubuntu11!!@localhost/mkt_base")
session = Session(bind=engine)
BASE_DIR = Path(__file__).resolve().parent.parent

Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id_mammoth = Column(BigInteger, nullable=False, unique=True)
    mammoth = Column(Text, nullable=False, unique=True)
    worker_id = Column(BigInteger, nullable=False)
    city = Column(Text, default=None)
    sale = Column(Float, default=0.0)


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    typee = Column(Text, nullable=False)  # central, outskirts, 2km, 5km


def insert_goods():
    g_1 = Goods(name='💎 ALFA PVP КР-WHITE + | 1 гр. | 🧲🚪| 2490р', price='2490', typee='central')
    g_2 = Goods(name='💎 ALFA PVP КР-WHITE + | 2 гр. | 🧲 | 4090р', price='4090', typee='central')
    g_3 = Goods(name='🧊 МЕФЕДРОН WHITE | 1 гр. | 🪨🚪| 3370р', price='3370', typee='central')
    g_34 = Goods(name='❄️ КОКАИН COLOMBIA | 2 гр. | 🪨🧲| 13090р', price='13090', typee='central')
    g_4 = Goods(name='🧊 МЕФЕДРОН WHITE | 2.2 гр. | 🪨 | 5200р', price='5200', typee='central')
    g_5 = Goods(name='🌰 ГАШИШ BLACK | 1 гр. | 🚪| 2800р', price='2800', typee='central')
    g_6 = Goods(name='🍚 БЕЛЫЙ CRYSS (A-PVP) + | 1 гр. | 🪨🚪🧲| 3600р', price='4090', typee='central')
    g_35 = Goods(name='АМФЕТАМИН 99% | 2 гр. | 🪨🧲| 4000р', price='4000', typee='central')
    g_33 = Goods(name='💉ГЕРОИН HQ KOLUMBIA | 1 гр. | 🪨🧲 | 3300р', price='3300', typee='central')
    g_32 = Goods(name='🌿МАРИХУАНА WHITE WINDOW | 3 гр. | 🧲 | 5500р', price='5500', typee='central')

    g_7 = Goods(name='💎 ALFA PVP КР-WHITE + | 1.1 гр. | 🧲🚪| 2490р', price='2490', typee='outskirts')
    g_36 = Goods(name='🍚 БЕЛЫЙ CRYSS (A-PVP) + | 10 гр. | 🪨🚪| 19500р', price='19500', typee='outskirts')
    g_9 = Goods(name='🧊 МЕФЕДРОН WHITE | 5 гр. | 🪨🚪🧲 | 8700р', price='8700', typee='outskirts')
    g_10 = Goods(name='🧊 МЕФЕДРОН WHITE | 2 гр. | 🪨 | 5200р', price='5200', typee='outskirts')
    g_11 = Goods(name='🌰 ГАШИШ BLACK | 1 гр. | 🚪| 2800р', price='2800', typee='outskirts')
    g_12 = Goods(name='🌰 ГАШИШ BLACK | 2 гр. | 🧲 | 4300р', price='4300', typee='outskirts')
    g_13 = Goods(name='💎 MDMA КРИС | 2 гр. | 🪨🚪| 4500р', price='4500', typee='outskirts')
    g_14 = Goods(name='❄️ КОКАИН COLOMBIA | 0.51 гр. | 🧲🪨🚪| 7090р', price='7090', typee='outskirts')
    g_15 = Goods(name='❄️ КОКАИН COLOMBIA | 2 гр. | 🪨🧲 | 13090р', price='13090', typee='outskirts')

    g_16 = Goods(name='🧊 МЕФЕДРОН WHITE | 2.1 гр. | 🧲🪨🚪| 5200р', price='5200', typee='2km')
    g_17 = Goods(name='🧊 МЕФЕДРОН WHITE | 1 гр. | 🪨 | 3370р', price='3370', typee='2km')
    g_18 = Goods(name='💎 MDMA КРИС | 2.2 гр. | 🧲 | 4500р', price='4500', typee='2km')
    g_19 = Goods(name=' 🌲Шишки OG KUSH | 2 гр. | 🚪| 2500р', price='2500', typee='2km')
    g_20 = Goods(name=' 🌲Шишки OG KUSH | 5 гр. | 🧲🚪| 4000р', price='4000', typee='2km')
    g_21 = Goods(name=' ️💉 ГЕРОИН HQ KOLUMBIA | 1 гр. | 🪨 | 3300р', price='3300', typee='2km')
    g_22 = Goods(name=' ️АМФЕТАМИН PINK | 1 гр. | 🪨 | 2100р', price='2100', typee='2km')

    g_23 = Goods(name='🧊 МЕФЕДРОН WHITE | 1 гр. | 🧲🪨 | 3370р', price='3370', typee='5km')
    g_24 = Goods(name='💊 ЭКСТАЗИ MAYBACH 240mg | 2 шт. | 🚪| 1890р', price='1890', typee='5km')
    g_25 = Goods(name='💊 ЭКСТАЗИ MAYBACH 240mg | 5 шт. | 🚪| 4500р', price='4500', typee='5km')
    g_26 = Goods(name='💎 ALFA PVP КР-WHITE + | 2 гр. | 🪨🧲| 4090р', price='4090', typee='5km')
    g_27 = Goods(name=' АМФЕТАМИН 99% | 2.1 гр. | 🧲🚪| 4000р', price='4000', typee='5km')
    g_28 = Goods(name='🌲Шишки OG KUSH | 2 гр. | 🪨🚪🧲| 2500р', price='2500', typee='5km')
    g_29 = Goods(name='🌿МАРИХУАНА WHITE WINDOW | 1 гр. | 🪨🧲🚪| 2100р', price='2100', typee='5km')
    g_30 = Goods(name='🌿МАРИХУАНА WHITE WINDOW | 2 гр. | 🚪| 3800р', price='3800', typee='5km')
    g_31 = Goods(name='💉 ГЕРОИН HQ KOLUMBIA | 0.51 гр. | 🧲🪨 | 2100р', price='2100', typee='5km')

    session.add_all([g_1, g_2, g_3, g_34, g_4, g_5, g_6, g_35, g_33, g_32, g_7, g_36, g_9, g_10, g_11, g_12, g_13, g_14, g_15, g_16, g_17, g_18, g_19, g_20, g_21, g_22, g_23, g_24, g_25, g_26, g_27, g_28, g_29, g_30, g_31])
    session.commit()

# insert_goods()
Base.metadata.create_all(engine)
