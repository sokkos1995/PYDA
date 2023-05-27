from sqlalchemy.orm import sessionmaker

from task1 import *

engine = sq.create_engine(DSN)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

# запросы
# принимает имя или идентификатор издателя (publisher), например, через input(). 
# Выводит построчно факты покупки книг этого издателя:
# название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
publisher_name = input('Введите имя издателя ')
# publisher_name = "O’Reilly"

q = session.query(Publisher.name, Shop.name, Sale.price, Sale.date_sale) \
                        .join(Book, Book.id_publisher == Publisher.id) \
                        .join(Stock, Stock.id_book == Book.id) \
                        .join(Shop, Stock.id_shop == Shop.id) \
                        .join(Sale, Sale.id_stock == Stock.id) \
                        .filter(Publisher.name == publisher_name)
print(q)
for s in q.all():
    print(s)




