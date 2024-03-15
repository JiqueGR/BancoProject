import requests

class Cotacao:

    @staticmethod
    def getCotacao(base='USD', symbols=['EUR']):
        url = f'https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL'
        response = requests.get(url)
        data = response.json()
        return data


