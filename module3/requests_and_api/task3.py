# url = 'https://api.stackexchange.com/docs/questions#fromdate=2023-03-03&order=desc&sort=activity&filter=default&site=stackoverflow'

# start_date = datetime.now() + timedelta(days=-2)
# start_date_unix = int(time.mktime(start_date.timetuple()))

# response = requests.get(url.format(unix_time=start_date_unix))
# print(response.json()['items'])


from datetime import datetime, timedelta
import time
import requests

class StackoverflowApi:

    def __init__(self):
        self.url = 'https://api.stackexchange.com/2.3/questions?fromdate={unix_time}&order=desc&sort=activity&site=stackoverflow'

    def make_start_date(self, days_ago):
        """ 
        Makes start date in unix format depending on today's date
        """
        start_date = datetime.now() + timedelta(days=-days_ago)
        return int(time.mktime(start_date.timetuple()))

    def get_questions(self, days_ago, tag):
        """ 
        Returns list of questions with requred tag
        """
        response = requests.get(self.url.format(unix_time=self.make_start_date(days_ago)))
        return [item['title'] for item in response.json()['items'] if tag in item['tags']]
