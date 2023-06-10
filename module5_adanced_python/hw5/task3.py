from task2 import logger
from hw2_main import run
# from ..hw2.main import run 

@logger('task3.log')
def decorated_hw2():
    run()

decorated_hw2()