import json
import random


class Quotes:
    def __init__(self, filename="data/quotes.json"):
        self.__filename = filename
        self.__open_and_read()

    def __open_and_read(self):
        """

        """
        # try to open file
        try:
            with open(self.__filename, 'r') as myfile:
                data = myfile.read()
        except FileNotFoundError:
            return False

        # parse file
        self.__quotes = json.loads(data)

    def get_random(self):
        """
        """
        num_quotes = len(self.__quotes)
        quote_num = random.randint(0, num_quotes)
        return self.__quotes[quote_num]
