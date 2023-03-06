import task1
import task2
import task3
import os

print("Задание 1")
c = task1.SuperheroesApi()
print(c.get_max_parametr('intelligence'))

print("Задание 2")
c = task2.YandexApi()
print(*c.get_files_list(), sep='\n')
path = os.path.dirname(__file__) + '/photo1.png'
c.upload_file_to_disk("netology/test", path)

print("Задание 3")
c = task3.StackoverflowApi()
print(*c.get_questions(2, 'python'), sep='\n')
