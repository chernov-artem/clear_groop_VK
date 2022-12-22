""" Парсит товары из группы ВК сохраняет их в текстовый файл вида: Название;цена;url   """

import vk_api
import time
import datetime
import tkinter
from tkinter import ttk
from tkinter import *


def gui_start():
    canvas.pack()
    frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.97)
    btn.place(relx=0.21, rely=0.37, height=25, width=85)
    text_area.place(relx=0.05, rely=0.02, height=50, width=245)
    text_area3.place(relx=0.03, rely=0.46, height=60, width=265)
    entry.place(relx=0.04, rely=0.22, height=20, width=140)


def btn_click():
    group_id = 0 - int(entry.get())
    res = market_get_goods_dict(group_id)
    file_name = f"goods_id{str(group_id)[1:]}_{str(datetime.datetime.now())[:-7].replace(' ', '_').replace(':', '-')}.txt"
    with open(str(file_name), "a+") as file:
        file.write("Muffin программы для бизнеса https://vk.com/muffin_programs_for_business\n\n")
        file.write("Содержание строчек:\n")
        file.write("Название товара;цена;ссылка на товар\n\n")
        for key, value in res.items():
            file.write(f"{value[0]};{value[1]};https://vk.com/market-215973925?w=product-215973925_{key}\n")
    root.quit()


def normal_price(s) -> int:
    """Получает цену из VK Api и возвращает её"""
    if len(s) <= 5:
        return int(s[:-2])
    else:
        price0 = s.split()
        price = int(price0[0] + price0[1][:-2])
        return price


def market_get_goods_dict(group_id):
    '''парсим товары группы и добавляем их все в словарь {id_товара : ['Название_товара', цена товара]}'''

    ''' Если число товаров < 200 используется 1 запрос. Если >200 используются запросы по 200 и 1 запрос на оставшуюся часть'''
    goods_dict = {}
    goods_00 = session.method('groups.getMembers', {'group_id': group_id, 'count': 5})
    count_of_goods = goods_00["count"]
    n = count_of_goods // 200
    np = count_of_goods % 200
    time.sleep(0.5)

    if count_of_goods <= 200:

        goods0 = session.method('market.get', {'owner_id': group_id, 'count': count_of_goods})

        for i in range(count_of_goods):
            price = normal_price(goods0['items'][i]['price']['text'])
            goods_dict[goods0['items'][i]['id']] = [goods0['items'][i]['title'], price]
    else:
        for i in range(n):
            shift = i * 200
            goods0 = session.method('market.get', {'owner_id': group_id, 'count': 200, 'offset': shift})
            for j in range(200):
                price = normal_price(goods0['items'][j]['price']['text'])
                goods_dict[goods0['items'][j]['id']] = [goods0['items'][j]['title'],
                                                        price]  # key словаря = id товара; value = [название товара, цена товара]

        shift = n * 200
        goods0 = session.method('market.get', {'owner_id': group_id, 'count': np, 'offset': shift})
        for i in range(np):
            price = normal_price(goods0['items'][i]['price']['text'])
            goods_dict[goods0['items'][i]['id']] = [goods0['items'][i]['title'],
                                                    price]

    return goods_dict


with open("token.txt", "r") as file:
    my_token = file.read()

# Блок GUI
root = Tk()
root['bg'] = '#fafafa'
root.title('Бэкап товаров группы ВК v 1.0 ')
root.geometry('340x280')

# переменные GUI
canvas = Canvas(root, height=640, width=480)
frame = Frame(root, bg='#c3c3c3')
btn = Button(frame, text='Запустить', bg='white', command=btn_click)
text_area = Label(frame, justify=LEFT, width=80, height=20, bg='#c3c3c3')
text_area['text'] = 'Вставьте id группы вконтакте,\nнажав Ctrl + V в английской раскладке [EN]:'
text_area3 = Label(frame, width=50, height=20, bg='#c3c3c3')
text_area3['text'] = 'После нажатия на кнопку\n результат будет записан в файл в этой же папке'
entry = Entry(frame, bg='white')

# блок VK-api
session = vk_api.VkApi(token=my_token)
vk = session.get_api()
gui_start()
root.mainloop()

if __name__ == '__main__':
    gui_start()
