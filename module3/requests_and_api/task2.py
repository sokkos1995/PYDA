import requests

class YandexApi:
    def __init__(self):
        self.token = 'y0_AgAAAABpEgt_AADLWwAAAADdwuBDESFUKa62RBGb8k_mjk--nsvgz-o'
        self.headers = {
                'Content-Type': 'application/json',
                'Authorization': 'OAuth {}'.format(self.token)
            }

    def get_files_list(self):
        """ 
        Returns list of objects in yandex disk
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        response = requests.get(url, headers=self.headers)
        return [el['name'] for el in response.json()['items']]

    def _get_upload_link(self, disk_file_path):
        """ 
        Makes an upload link so file can be stored there
        """
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=self.headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        """ 
        Takes path for storing file in YandexDisk and stores a file there
        """
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

