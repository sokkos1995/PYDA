import requests
import os

class FilesParser:

    def get_paths(self):
        """ 
        
        """
        files_path = os.path.join(os.path.dirname(__file__), 'files', 'sorted')
        list_of_paths = list()
        for el in os.listdir(path=files_path):
            file_path = os.path.join(files_path, el)
            list_of_paths.append(file_path)
        return list_of_paths  

    def make_list_with_metadata_url(self, URL):
        """ 
        Takes file by its url and parses it. 
        Result contains file name, number of strings and all strings.
        Example of result:
        ['file_name.txt', 1, 'string number 1', 'string number 2']
        """
        response = requests.get(URL)
        return [URL.split('/')[-1], len(response.text.strip().split('\n'))] + response.text.strip().split('\n')

    def make_list_with_metadata_path(self, path):
        """ 
        Takes file by its path and parses it. 
        Result contains file name, number of strings and all strings.
        Example of result:
        ['file_name.txt', 1, 'string number 1', 'string number 2']
        """
        with open(path) as f:
            strings = f.readlines()
        return [path.split('/')[-1], len(strings)] + [el.strip() for el in strings]       


# Первый способ - файлы расположены не локально (забираем их по url-ам )
if __name__ == '__main__':
    URL1 = r'https://raw.githubusercontent.com/netology-code/py-homework-basic-files/master/2.4.files/sorted/1.txt'
    URL2 = r'https://raw.githubusercontent.com/netology-code/py-homework-basic-files/master/2.4.files/sorted/2.txt'
    URL3 = r'https://raw.githubusercontent.com/netology-code/py-homework-basic-files/master/2.4.files/sorted/3.txt'
    url_list, list_of_files = [URL1, URL2, URL3], []

    for url in url_list:
        file = FilesParser()
        file = file.make_list_with_metadata_url(url)
        list_of_files.append(file)
    list_of_files = sorted(list_of_files, key=lambda file: file[1])
    for file in list_of_files:
        print(*file, sep='\n')

# Второй способ - файлы расположены локально
if __name__ == '__main__':
    file_class = FilesParser()
    list_of_paths, list_of_files = file_class.get_paths(), list()
    for path in list_of_paths:
        file = file_class.make_list_with_metadata_path(path)
        list_of_files.append(file)
    list_of_files = sorted(list_of_files, key=lambda file: file[1])
    for file in list_of_files:
        print(*file, sep='\n')