import requests
from bs4 import BeautifulSoup


desired_tags = {'мы', 'javascript', 'java', 'python', 'компьютер'}

response = requests.get('https://habr.com/ru/all/')
if not response.ok:
    raise ValueError('response is not valid')
soup = BeautifulSoup(response.text, 'html.parser')

# href_list = []

for article in soup.find_all('article'):

    hubs = {h.text.lower() for h in article.find_all('a', class_='hub-link')}  # генератор множества? хабов))
    # print(hubs)  # {'Системное администрирование', 'Софт'} - пример, все хабы

    title = article.find('h2', class_='post__title')

    head = title.find(class_='post__title_link').text   # заголовок статьи
    # print(head)

    if hubs & desired_tags:
        print(f'Совпадение по тегу - {hubs & desired_tags}')
        href = title.find('a').attrs.get('href')  # ссылка на статью

        header = article.find('header', class_='post__meta')
        time = header.find('span', class_='post__time').text  # время статьи

        print(f'<{time}>, <{head}>, <{href}>')
        continue

    wall = article.find('div', class_='post__body post__body_crop').text  # текст превью статьи
    # print(wall)

    status_match = False
    for hub in desired_tags:
        if hub in wall.lower() or hub in head.lower():
            status_match = True
            print(f"Совпадение в заголовке или в превью - {{'{hub}'}}")

            href = title.find('a').attrs.get('href')  # ссылка на статью

            header = article.find('header', class_='post__meta')
            time = header.find('span', class_='post__time').text  # время статьи

            print(f'<{time}>, <{head}>, <{href}>')
            break

    if status_match:
        continue
