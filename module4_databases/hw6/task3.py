import json
import os
from pprint import pprint

from sqlalchemy.orm import sessionmaker

from task1 import *

path = os.path.dirname(__file__) + '/tests_data.json'
with open(path, "r") as f:
    test_data = json.load(f)

test_data_dict = {}

for el in test_data:
    table_name = el['model']
    test_data_dict.setdefault(table_name, [])
    del(el['model'])
    el = {'pk': el['pk'], **el['fields']}
    test_data_dict[table_name].append(el)

# pprint(test_data_dict)  

# сессия
Session = sessionmaker(bind=engine)
session = Session()

# создание объектов

def add_book(list_of_books=[]):
    """ 
    Функция для добавления книг в БД
    """
    session.add_all([Book(id=book['pk'], 
                    title=book['title'], 
                    id_publisher=book['id_publisher']) for book in list_of_books])
    session.commit()
    print('books added')

def add_publisher(list_of_publishers=[]):
    """ 
    Функция для добавления издателей в БД
    """
    session.add_all([Publisher(id=publisher['pk'], 
                    name=publisher['name']) for publisher in list_of_publishers])
    session.commit()
    print('publishers added')

def add_shop(list_of_shops=[]):
    """ 
    Функция для добавления издателей в БД
    """
    session.add_all([Shop(id=shop['pk'], 
                    name=shop['name']) for shop in list_of_shops])
    session.commit()
    print('shops added')

def add_stock(list_of_stocks=[]):
    """ 
    Функция для добавления издателей в БД
    """
    session.add_all([Stock(id=stock['pk'],
                    id_shop=stock['id_shop'],
                    id_book=stock['id_book'],
                    count=stock['count']) for stock in list_of_stocks])
    session.commit()
    print('stocks added')

def add_sale(list_of_sales=[]):
    """ 
    Функция для добавления издателей в БД
    """
    session.add_all([Sale(id=sale['pk'],
                    price=sale['price'],
                    id_stock=sale['id_stock'],
                    date_sale=sale['date_sale'],
                    count=sale['count']) for sale in list_of_sales])
    session.commit()
    print('sales added')


add_publisher(test_data_dict['publisher'])
add_book(test_data_dict['book'])
add_shop(test_data_dict['shop'])
add_stock(test_data_dict['stock'])
add_sale(test_data_dict['sale'])