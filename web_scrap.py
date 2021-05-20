import requests
from bs4 import BeautifulSoup


desired_tags = {'javascript', 'python', 'сервер'}  # слово сервер - часто встречается в самой статье))

response = requests.get('https://habr.com/ru/all/')
if not response.ok:
    raise ValueError('response is not valid')
soup = BeautifulSoup(response.text, 'html.parser')

for article in soup.find_all('article'):

    hubs = {h.text.lower() for h in article.find_all('a', class_='hub-link')}  # генератор множества? хабов))
    # print(hubs)  # {'Системное администрирование', 'Софт'} - пример, все хабы

    title = article.find('h2', class_='post__title')

    head = title.find(class_='post__title_link').text   # заголовок статьи

    href = title.find('a').attrs.get('href')  # ссылка на статью

    hubs_match = True  # флаг для ускорения поиска - нашлось совпадение по хабам
    head_preview_match = False  # совпадение по head  или статья
    page_body_match = False  # совпадение только в самой статье после перехода на неё

    if not hubs & desired_tags:
        hubs_match = False
        wall = article.find('div', class_='post__body post__body_crop').text  # текст превью статьи

        for hub in desired_tags:
            if hub in wall.lower() or hub in head.lower():
                head_preview_match = True
                matched_head_preview_hub = hub
                break

        if not head_preview_match:

            article_page = requests.get(href)
            if not article_page.ok:
                raise ValueError('response is not valid')
            soup_page = BeautifulSoup(article_page.text, 'html.parser')

            article_data = soup_page.find('article')
            content = article_data.find('div', class_='post__body post__body_full').text.lower()

            for hub in desired_tags:
                if hub in content:
                    page_body_match = True
                    matched_body_hub = hub
                    break

    if head_preview_match:
        print(f"Совпадение в заголовке или в превью - {{'{matched_head_preview_hub}'}}")
    elif hubs_match:
        print(f'Совпадение по тегу - {hubs & desired_tags}')
    elif page_body_match:
        print(f"Совпадение в самой статье - {{'{matched_body_hub}'}}")
    else:
        continue

    time_head = article.find('header', class_='post__meta')
    time = time_head.find('span', class_='post__time').text  # время статьи

    print(f'<{time}>, <{head}>, <{href}>')
