from datetime import datetime,timedelta
from statistics import mean
import urllib.request
import xml.dom.minidom as minidom

#получаем данные по url
def get_data(xml_url):
    try:
        web_file = urllib.request.urlopen(xml_url)
        return web_file.read()
    except:
        pass
#функция для создания словаря название валюты - значение для каждого дня
def get_current_dictionary(xml_content):

    dom = minidom.parseString(xml_content)
    dom.normalize()

    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Nominal':
                    if child.firstChild.nodeType == 3:
                        nominal = int(child.firstChild.data)
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = round(float(child.firstChild.data.replace(',', '.') ) / nominal, 5)
                if child.tagName == 'Name':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value
    return currency_dict

today = datetime.now() #дата запуска программы
date = today - timedelta(90) #за 90 дней до запуска
#переменные
min_value = 10000
min_name = ''
max_value = 0
max_name= ''
min_date=''
max_date =''
all_values=[]


for i in range(90):
    #создаем необходимый для даты url
    url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(date.strftime('%d/%m/%Y'))
    # словарь название - значение на текущую дату
    currency_dict = get_current_dictionary(get_data(url))
    #минимальное и максимальное значение на текущую дату
    current_min= min(currency_dict.values())
    current_max = max(currency_dict.values())
    #пополняем список всех значений
    all_values += currency_dict.values()


    rd = {}
    for k, v in currency_dict.items():
        rd[v] = rd.get(v, []) + [k]

    if current_min<min_value:
        min_value = current_min
        min_date = date
        min_name = rd.get(min_value)
    if current_max > max_value:
        max_value = current_max
        max_date = date
        max_name = rd.get(max_value)
    #переходим к следующему дню
    date += timedelta(1)

print("Среднее значение курса рубля за весь период по всем валютам: " + str(round(mean(all_values),3)))
print('Максимальный курс валюты : '+ str(max_value) + " Дата: " + str(max_date.strftime('%d/%m/%Y')) + " Название: " + str(*max_name))
print('Минимальный курс валюты : '+ str(min_value) + " Дата: " + str(min_date.strftime('%d/%m/%Y')) + " Название: " + str(*min_name))

input()