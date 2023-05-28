from datetime import date
import os

from application.salary import calculate_salary
from application.db.people import get_employees


if __name__ == '__main__':
    print("Today's date", date.today(), end='\n\n')
    calculate_salary()
    get_employees()

    path = os.path.dirname(__file__) + '/requirements.txt'
    with open(path, 'r') as f:
        for line in f:
            print('command for terminal insert: pip install', line)