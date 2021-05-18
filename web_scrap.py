import requests
from bs4 import BeautifulSoup


desired_tags = {'JavaScript', 'Java', 'IT-компании', 'Python'}

response = requests.get('https://habr.com/ru/all/')
if not response.ok:
    raise ValueError('response is not valid')
soup = BeautifulSoup(response.text, 'html.parser')

# href_list = []

for article in soup.find_all('article'):

    hubs = {h.text for h in article.find_all('a', class_='hub-link')}
    # print(hubs)

    if hubs & desired_tags:
        print(hubs & desired_tags)  # добавил чтобы было понятно, какой из тэгов сработал
        title = article.find('h2', class_='post__title')
        href = title.find('a').attrs.get('href')
        # href_list.append(href)

        head = title.find(class_='post__title_link').text
        # print(head)

        header = article.find('header', class_='post__meta')
        time = header.find('span', class_='post__time').text
        # print(time)

        print(f'<{time}>, <{head}>, <{href}>')
