from bs4 import BeautifulSoup
import requests
from itertools import groupby


def save(line, full_link):
	with open('D:\\python\\parser\\LapTop.txt', 'a', encoding='utf-8') as file:
		file.write(f'Модель {teh["title"]} -> ' + setTabs(line) +f'\nХарактеристики -> {teh["character"].capitalize()}\nСсыкла на товар -> ' + f'{doFulLink(full_link)}\n')

def setTabs(line):
	if len(line) == 25:
		firstSpace = line[0:7]
		minPrice = line[7:14]
		maxPrice = line[16:23]
		secondSpace = line[14:16]
		v = (f'{firstSpace} {minPrice} {secondSpace} {maxPrice}')
	else:
		firstSpace = line[0:7]
		minPrice = line[7:13]
		maxPrice = line[15:23]
		secondSpace = line[13:15]
		v = (f'{firstSpace} {minPrice} {secondSpace} {maxPrice}')
	return v 


def doFulLink(full_link):
	flink = 'https://www.e-katalog.ru' + full_link
	return flink

def parser():
	line = ''
	max_pages = 43
	count = 0

	for x in range(2, max_pages):
		URL = 'https://www.e-katalog.ru/list/298/' + str(x) + '/'

		HEADERS = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
		}

		#Отправляем запрос на страницу
		resopne = requests.get(URL, headers = HEADERS)
		#Получаем контент со страницы
		soup = BeautifulSoup(resopne.content, 'html.parser')
		items = soup.findAll('div', class_ = 'model-short-div list-item--goods-group ms-grp')

		#Пустой массив для записи данных в него
		tehs = []

		for item in items:
			tehs.append({
				'title': item.find('a', class_ = 'no-u').get_text(strip = True),
				'price': item.find('div', class_ = 'model-price-range').get_text(strip = True),
				'character': item.find('ul', class_ = 'conf-key-prop clearfix').get_text(strip = True),
				'link': item.find('a', class_ = 'no-u').get('href')
				})

		new_tehs = [el for el, _ in groupby(tehs)] #Удаляем повторные элементы из массива
		

		global teh
		for teh in new_tehs: #Перебираем элементы в массиве
			count += 1
			line = teh["price"] #В line передаем цену на товар
			#scyde = setTabs(line) #Вызываем функцию
			full_link = teh["link"] #Передаем ссылку в full_link
			print(f'Модель {teh["title"]} -> ' + setTabs(line) +f'\nХарактеристики -> {teh["character"].capitalize()}\nСсыкла на товар -> ' + doFulLink(full_link) + '\n')
			save(line, full_link)


		#print(f'Всего ноутбуков показано {count}')

parser()

