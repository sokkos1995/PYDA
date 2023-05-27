import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

    # homeworks = relationship("Homework", back_populates="course")

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    # course = relationship(Course, back_populates="homeworks")
    # Publisher = relationship(Publisher, backref="id_publisher")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

    # homeworks = relationship("Homework", back_populates="course")

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # course = relationship(Course, back_populates="homeworks")
    # Book = relationship(Book, backref="id_book")   
    # Shop = relationship(Shop, backref="id_shop")     

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # course = relationship(Course, back_populates="homeworks")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = "postgresql://postgres:postgrespw@localhost:5432/diploma"
engine = sq.create_engine(DSN)

if __name__ == '__main__':
    engine = sq.create_engine(DSN)
    create_tables(engine)