import os.path

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'coffee.db')

Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    item_id = Column(Integer, ForeignKey('menu.id'),nullable=False)
    cups = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        menu_items = [
            {"name": "Американо", "price": 149,
             "description": "Американо - напиток, приготовленный путём разбавления эспрессо горячей водой в определённой пропорции."},
            {"name": "Раф", "price": 211,
             "description": "Раф - популярный российский кофейный напиток, который готовят на основе эспрессо с добавлением ванильного и простого сахара, а также сливок."},
            {"name": "Латте", "price": 219,
             "description": "Латте - кофейный напиток на основе молока, представляющий собой трёхслойную смесь из молочной пены, молока и кофе эспрессо."},
            {"name": "Капучино", "price": 189,
             "description": "Капучино - кофейный напиток итальянской кухни на основе эспрессо с добавлением в него подогретого до 65 градусов вспененного молока."}
        ]
        for item in menu_items:
            if not session.query(Menu).filter_by(name=item["name"]).first():
                session.add(Menu(name=item["name"], price=item["price"], description=item["description"]))
        session.commit()
