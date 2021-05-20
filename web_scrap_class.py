import requests
from bs4 import BeautifulSoup


class HabrScrapper:
    def __init__(self):
        self.DESIRED_TAGS = {'javascript', 'python', 'java', 'сервер'}  # сервер - часто встречается в самой статье))
        self.match_hubs, self.match_head_preview, self.match_page = False, False, False  # флаги совпадений
        self.hubs_tags = None

    @staticmethod
    def get_url(url):
        response = requests.get(url)
        if not response.ok:
            raise ValueError('response is not valid')
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    @staticmethod
    def hubs_gen(article):
        hubs = {h.text.lower() for h in article.find_all('a', class_='hub-link')}  # генератор множества? хабов))
        return hubs

    def are_desired_tags_in_hubs(self, hubs):
        self.hubs_tags = hubs & self.DESIRED_TAGS
        if self.hubs_tags:
            return True
        return False

    def is_in_page_or_head(self, page: str, head=None):
        """page - превью или тело самой статьи, head - заголовок"""
        for hub in self.DESIRED_TAGS:
            if hub in page.lower() or (head and hub in head.lower()):
                return True, hub
        return False, None

    def printer(self, article, head, href, match_head_preview_hub, matched_hub_page):
        if self.match_hubs:
            print(f'Совпадение по тегу - {self.hubs_tags}')
        elif self.match_head_preview:
            print(f"Совпадение в заголовке или в превью - {{'{match_head_preview_hub}'}}")
        elif self.match_page:
            print(f"Совпадение в самой статье - {{'{matched_hub_page}'}}")
        else:
            return

        time_head = article.find('header', class_='post__meta')
        time = time_head.find('span', class_='post__time').text  # время статьи

        print(f'<{time}>, <{head}>, <{href}>\n')

    def parser(self):
        soup = self.get_url('https://habr.com/ru/all/')

        for article in soup.find_all('article'):
            hubs = self.hubs_gen(article)

            title = article.find('h2', class_='post__title')
            head = title.find(class_='post__title_link').text  # заголовок статьи
            href = title.find('a').attrs.get('href')  # ссылка на статью

            self.match_hubs = self.are_desired_tags_in_hubs(hubs)
            if not self.match_hubs:
                wall = article.find('div', class_='post__body post__body_crop').text  # текст превью статьи
                self.match_head_preview, match_head_preview_hub = self.is_in_page_or_head(wall, head)
                if not self.match_head_preview:
                    soup_article = self.get_url(href)

                    article_data = soup_article.find('article')
                    content = article_data.find('div', class_='post__body post__body_full').text.lower()
                    self.match_page, matched_hub_page = self.is_in_page_or_head(content)

            self.printer(article, head, href, match_head_preview_hub, matched_hub_page)


if __name__ == '__main__':
    habr = HabrScrapper()
    habr.parser()
