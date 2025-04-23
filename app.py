import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from datetime import date
import time
import pytz


load_dotenv()

def send_message(data):

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHANEL_ID = os.getenv('TELEGRAM_CHANEL_ID')

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

    params = {
        'chat_id': TELEGRAM_CHANEL_ID,
        'text': data
    }
    res = requests.get(url, params=params)
    return res.json()





if __name__ == '__main__':

    langs = [ 'ru', 'ja', 'ko', 'uk', 'id', 'de', 'en', 'it', 'vi', 'he', 'th' ]
    titles = ['Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'פלייריקס','เพลย์ริกซ์']
    ids = ['1753369', '3827363', '2828727', '2377222', '3984678', '10941028', '52668348', '9036946', '19357370', '2112701', '1349692']

    dataset = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    pravki = 0
    news = []

    for k in range(len(langs)):
        time.sleep(1)
        url = f'https://{langs[k]}.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'revisions',
            'titles': f'{titles[k]}'
        }
        
        response = requests.get(url, params=params)
        data = response.json()

        # Доступ к данным об изменениях
        revisions = data['query']['pages'][f'{ids[k]}']['revisions']
        print(datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d'))
        for revision in revisions:
            if str(datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d')) == revision['timestamp'].split('T')[0]:
                pravki = pravki + 1
                news.append(f'https://{langs[k]}.wikipedia.org/w/index.php?title={titles[k]}&action=history')
                
                
        dataset[k][0] = f'https://{langs[k]}.wikipedia.org/w/index.php?title={titles[k]}&action=history'
        dataset[k][1] = revision['timestamp'].split('T')[0]
    
    if pravki > 0:
        send_message(str(datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S'))+' / Есть свежие правки:\n')
        for h in range(len(news)):
            print(news[h])
            send_message(news[h]+'\n')
    else:
        send_message(str(datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S'))+' / Свежих правок не было:\n')
        
    send_message(
        'Ссылка'+' / '+'Дата последней правки'+'\n'+
        dataset[0][0]+'   '+dataset[0][1]+'\n'+
        dataset[1][0]+'   '+dataset[1][1]+'\n'+
        dataset[2][0]+'   '+dataset[2][1]+'\n'+
        dataset[3][0]+'   '+dataset[3][1]+'\n'+
        dataset[4][0]+'   '+dataset[4][1]+'\n'+
        dataset[5][0]+'   '+dataset[5][1]+'\n'+
        dataset[6][0]+'   '+dataset[6][1]+'\n'+
        dataset[7][0]+'   '+dataset[7][1]+'\n'+
        dataset[8][0]+'   '+dataset[8][1]+'\n'+
        dataset[9][0]+'   '+dataset[9][1]+'\n'+
        dataset[10][0]+'   '+dataset[10][1]+'\n'
    )