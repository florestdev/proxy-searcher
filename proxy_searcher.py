import requests
from bs4 import BeautifulSoup
import sys, pathlib

print(f'FLORESTDEV\nДанная программа чекает список публичных прокси серверов.\nВсе доступные прокси серверы будут в файле `proxies.txt`.')

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup.textarea.text.split('\n')[3:-1]

def test_proxies(proxies: list):
    print(f'Обнаружено бесплатных прокси - {len(proxies)}:')
    proxies_ = []
    for prox in proxies:
        try:
            req = requests.get('https://ip.beget.ru/', proxies={"http":f'http://{prox}', 'https':f'http://{prox}'}, timeout=0.5)
            if req.status_code == 200:
                print(f'Доступный прокси: {prox}')
                proxies_.append(prox)
            else:
                print(f'{prox} недоступен.')
        except:
            print(f'{prox} недоступен.')
    with open(pathlib.Path(sys.argv[0]).parent.resolve() / 'proxies.txt', 'w') as file:
        if len(proxies_) == 0:
            file.write(f'Нет доступных прокси на данный момент.')
            file.close()
        else:
            file.write(proxies_)
            file.close()

if __name__ == '__main__':
    test_proxies(get_free_proxies())