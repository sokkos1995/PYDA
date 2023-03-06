import requests

class SuperheroesApi:

    def __init__(self):
        self.url = r'https://akabab.github.io/superhero-api/api'
        self.superheroes_intelligence = dict()
    
    def get_max_parametr(self, parametr):
        """
        Return name of hero with maximum powerstst parametr.
        May be such parametrs as:
        intelligence, strength, speed, durability, power, combat
        """
        response = requests.get(self.url + r'/all.json')
        for el in response.json():
            if el['name'] in ('Hulk','Captain America', 'Thanos'):
                self.superheroes_intelligence[el['name']] = el['powerstats'][parametr]

        for key, value in self.superheroes_intelligence.items():
            if value == max(self.superheroes_intelligence.values()):
                hero = key
        return hero