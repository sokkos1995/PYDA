from pprint import pprint
import requests
import os

class CookBook:

    def __init__(self, URL=''):
        self.URL = URL
        self.cook_book = {}
    
    def make_cook_book_from_url(self):
        """ 
        Take data from remote file.txt by its url and make cook_book.
        Example of structure:
        {
        'Омлет': [{'ingredient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт'},
           {'ingredient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
           {'ingredient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}]
        }
        """
        res = requests.get(self.URL)
        for dish in res.text.split('\n\n'):
            dish = dish.split('\n')
            key, value = dish[0], []
            for i in range(int(dish[1])):
                ingridient = {}
                ingridient_list = dish[2 + i].split(' | ')
                ingridient['ingredient_name'] = ingridient_list[0]
                ingridient['quantity'] = int(ingridient_list[1])
                ingridient['measure'] = ingridient_list[2]
                value.append(ingridient)
            self.cook_book[key] = value
        return self.cook_book

    def get_shop_list_by_dishes(self, dishes, person_count):
        """ 
        Forms shops list depending on list of dishes and number of persons.
        Example of structure:
        {
        'Картофель': {'measure': 'кг', 'quantity': 2},
        'Молоко': {'measure': 'мл', 'quantity': 200},
        'Помидор': {'measure': 'шт', 'quantity': 4},
        'Сыр гауда': {'measure': 'г', 'quantity': 200},
        'Яйцо': {'measure': 'шт', 'quantity': 4},
        'Чеснок': {'measure': 'зубч', 'quantity': 6}
        }
        """
        shop_list = dict()
        for dish in dishes:
            for ingridient in self.cook_book[dish]:
                if ingridient not in list(shop_list.keys()):
                    value = dict()
                    value['measure'], value['quantity'] = ingridient['measure'], person_count * ingridient['quantity']
                    shop_list[ingridient['ingredient_name']] = value
                else:
                    shop_list['ingredient_name']['quantity'] += person_count * ingridient['quantity']
        return shop_list

if __name__ == '__main__':
    URL = r'https://raw.githubusercontent.com/netology-code/py-homework-basic-files/master/2.4.files/recipes.txt'
    task1 = CookBook(URL=URL)
    print('Задание 1')
    pprint(task1.make_cook_book_from_url(), sort_dicts=False)
    print('Задание 2')
    pprint(task1.get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))