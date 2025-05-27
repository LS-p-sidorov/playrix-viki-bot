import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
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

    langs = ['ru', 'en', 'id', 'he', 'uk', 'ru', 'en', 'id', 'he', 'ru', 'ja', 'ko', 'uk', 'de', 'en', 'it', 'vi']
    titles = ['Бухман, Дмитрий Анатольевич', 'Dmitry Bukhman', 'Dmitry Bukhman', 'דמיטרי בוכמן', 'Бухман Ігор Анатолійович', 'Бухман, Игорь Анатольевич', 'Igor Bukhman', 'Igor Bukhman', 'איגור בוכמן', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix', 'Playrix']
    ids = ['8049948', '62661703', '4261400', '2326524', '3411941', '8049954', '70596728', '4261416', '2326829', '1753369', '3827363', '2828727', '2377222', '10941028', '52668348', '9036946', '19357370']

    dataset = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    pravki = 0
    news = []

    yestarday = datetime.now(pytz.timezone('Europe/Moscow'))-timedelta(days=1)
    yestarday = yestarday.strftime('%Y-%m-%d')

    today = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d')

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

        for revision in revisions:
            if str(today) == revision['timestamp'].split('T')[0] or str(yestarday) == revision['timestamp'].split('T')[0]:
                pravki = pravki + 1
                news.append(f'https://{langs[k]}.wikipedia.org/w/index.php?title={titles[k]}&action=history'.replace(' ','_'))
                
                
        dataset[k][0] = f'https://{langs[k]}.wikipedia.org/w/index.php?title={titles[k]}&action=history'.replace(' ','_')
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
        dataset[10][0]+'   '+dataset[10][1]+'\n'+
        dataset[11][0]+'   '+dataset[11][1]+'\n'+
        dataset[12][0]+'   '+dataset[12][1]+'\n'+
        dataset[13][0]+'   '+dataset[13][1]+'\n'+
        dataset[14][0]+'   '+dataset[14][1]+'\n'+
        dataset[15][0]+'   '+dataset[15][1]+'\n'
    )