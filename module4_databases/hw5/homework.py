import psycopg2 as pg
import logging
import os

class DBLoader:

    def __init__(self):
        pass

    def create_table(self, cursor, query):
        """ 
        Создает таблицы в базе данных.  
        """
        print("executing query ", query)
        # cursor.execute(query)
        try:
            cursor.execute(query)
            conn.commit()
        except:
            print("Что то пошло не так.")

    def add_client(self, cursor, params):
        """ 
        Функция, позволяющая добавить нового клиента.
        Обычно данные приходят нам автоматизированно, через АПИ, в формате json.
        Данная функция преобразует json в insert query.
        """
        pass

    def add_phone(self):
        """ 
        
        """
        pass

    def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
        pass

    def delete_phone(conn, client_id, phone):
        pass

    def delete_client(conn, client_id):
        pass

    def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
        pass    

sql_1 = """ 
create table clients (
	name varchar(100),
	surname varchar(100),
	email varchar(100),
	phone_number varchar(100)
);
"""

sql2 = """ 
insert into client 
values
('konstantin', 'sokolov', 'email@gmail.ru', '555-35-35')
"""


if __name__ == '__main__':
    loader = DBLoader()
    conn = pg.connect(host='127.0.0.1',
                    port='5432',
                    database="diploma", 
                    user="postgres", 
                    password="postgrespw")
    cur = conn.cursor()
    loader.create_table(cur, sql_1)
    conn.close()

