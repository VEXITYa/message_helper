import vk_api
import time
from collections import OrderedDict
from datetime import datetime

flag = True
while flag:
    tok = ''
    msg = ''
    intr = -1
    if tok == '':
        tok = input('Введите токен: ')
    if msg == '':
        msg = input('Введите сообщение: ')
    if intr == -1:
        while intr > 600 or intr < 0:
            intr = int(input('Введите интервал: '))
            if intr < 0:
                print("Интервал должен быть положительным числом")
            elif intr > 600:
                print("Слишком большой интервал")
            else:
                break

    logs = open('data/logs.txt', 'w')
    with open('data/ids.txt', 'r') as f:
        ids = f.read().splitlines()

    try:
        vk_session = vk_api.VkApi(token=tok)
        vk_session._auth_token()
        vk = vk_session.get_api()
        a = []
        print("-" * 70)
        for x in ids:
            if x not in a:
                vk.messages.send(chat_id=int(x), message=msg, random_id=0)
                t = str(datetime.now())[0:19]
                title = vk.messages.getChat(chat_id=int(x))["title"]
                tmp_msg = msg
                if len(title) > 15:
                    title = title[0:15] + "..."
                if len(msg) > 20:
                    tmp_msg = tmp_msg[0:20] + "..."
                title = (title + " " * 30)[:20]
                ans = title + " : " + tmp_msg
                ans = (ans + " " * 50)[:50]
                print(ans, t)
                a.append(x)
                time.sleep(intr)
        print("-" * 70)
        flag = False
    except BaseException:
        print("ERROR")