# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import vk_api
import time
import pickle
from collections import OrderedDict
from datetime import datetime

AUTH_FILE = 'data/auth.txt'
flag = True


def sendmsg(chat_id, messag):
    vk.messages.send(chat_id=int(chat_id), message=messag, random_id=0)
    t = str(datetime.now())[0:19]
    title = vk.messages.getChat(chat_id=int(chat_id))["title"]
    tmp_msg = messag
    if len(title) > 15:
        title = title[0:15] + "..."
    if len(messag) > 20:
        tmp_msg = tmp_msg[0:20] + "..."
    title = (title + " " * 30)[:20]
    ans = title + " : " + tmp_msg
    ans = (ans + " " * 50)[:50]
    return str(ans + t)


def get_saved_auth_params():
    access_token = None
    try:
        with open(AUTH_FILE, 'rb') as pkl_file:
            access_token = pickle.load(pkl_file)
    except IOError:
        pass
    return access_token


def save_auth_params(access_token):
    with open(AUTH_FILE, 'wb') as output:
        pickle.dump(access_token, output)


while flag:
    msg = None
    intr = None
    tok = get_saved_auth_params()
    if not tok:
        tok = input("Введите токен: ")
    else:
        s = input("Хотите сменить токен?(y/n): ").lower()
        if s == 'y':
            tok = input("Введите токен: ")
    save_auth_params(tok)
    if not msg:
        msg = input('Введите сообщение: ')
    if not intr:
        while not intr or intr > 600 or intr < 0:
            intr = int(input('Введите интервал: '))
            if intr < 0:
                print("Интервал должен быть положительным числом")
            elif intr > 600:
                print("Слишком большой интервал")
            else:
                break

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
                otv = sendmsg(x, msg)
                print(otv)
                a.append(x)
                time.sleep(intr)
        print("-" * 70)
        flag = False
    except BaseException:
        print("\nERROR")
