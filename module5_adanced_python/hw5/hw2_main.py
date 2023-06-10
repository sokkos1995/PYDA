from pprint import pprint
import csv
import re
import os

def fix_commas(contacts_list):
    """ 
    Функция, которая делает убирает лишние поля (приводит в соответствие с заголовком csv)
    """
    correct_length = len(contacts_list[0])
    for index, contact in enumerate(contacts_list):  # есть строка с лишней запятой, для 
        contacts_list[index] = contact[:correct_length]  


def fix_name(contacts_list):
    """ 
    Функция, которая с помощью регулярных выражений разбивает фио 
    по 3 колонкам в списке контактов.
    """
    for row in contacts_list[1:]:
        fio = re.search(r'([а-я]+[ин|ов|ев]а?) ([а-я]+) ?([а-я]+[ич|вна])?', ' '.join(row[:3]).strip(), flags=re.I)
        row[0], row[1], row[2] = fio.group(1), fio.group(2), fio.group(3)      

def fix_phone(contacts_list):
    """
    Функция, которая приводит телефоны в списке контактов к единому формату
    """
    for row in contacts_list[1:]:
        row[5] = re.sub( r'(\+?[7|8])? ?\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{2})[ -]?(\d{2}) ?\(?(доб.\)?)? ?(\d{4})?\)?', r'+7(\2)\3-\4-\5 \6\7' , row[5])
        row[5] = row[5].strip()    

def merge_contacts(contacts_list):
    """ 
    Функция, которая "схлопывает" повторяющиеся контакты
    """
    surnames = {}
    fixed_list = [contacts_list[0]]

    for index, row in enumerate(contacts_list[1:]):
        if row[0] not in surnames.keys():
            surnames[row[0]] = index + 1
            
        else:
            fix_row = contacts_list[surnames[row[0]]]
            for i in range(1,7):
                fix_row[i] = fix_row[i] or row[i]

    for index in surnames.values():
        fixed_list.append(contacts_list[index])

    return fixed_list
    


# if __name__ == '__main__': 

def run():
    path = os.path.dirname(__file__)

    with open(path + "/phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts = list(rows)

        fix_commas(contacts)
        fix_name(contacts)
        fix_phone(contacts)
        contacts = merge_contacts(contacts)

    with open(path + "/phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')        
        datawriter.writerows(contacts)

if __name__ == '__main__':
    run()