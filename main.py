import requests
from bs4 import BeautifulSoup
from time import sleep
import random

# Настройки
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]


def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    }


def parse_pikabu(page_count=1):
    base_url = "https://pikabu.ru/hot"
    results = []

    for page in range(1, page_count + 1):
        try:
            url = f"{base_url}?page={page}" if page > 1 else base_url
            print(f"Парсинг страницы {url}")

            response = requests.get(url, headers=get_random_headers(), timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article', class_='story')

            for article in articles:
                try:
                    title = article.find('h2', class_='story__title').text.strip()
                    link = "https://pikabu.ru" + article.find('a', class_='story__title-link')['href']
                    rating = article.find('div', class_='story__rating-count').text.strip()
                    comments = article.find('span', class_='story__comments-link-count').text.strip()
                    author = article.find('a', class_='user__nick').text.strip()

                    results.append({
                        'title': title,
                        'link': link,
                        'rating': rating,
                        'comments': comments,
                        'author': author
                    })
                except Exception as e:
                    print(f"Ошибка парсинга статьи: {e}")
                    continue

            sleep(random.uniform(1.5, 3.0))

        except Exception as e:
            print(f"Ошибка при обработке страницы {page}: {e}")
            break

    return results


if __name__ == "__main__":
    parsed_data = parse_pikabu(page_count=2)  # Парсим 2 страницы

    print("\nРезультаты парсинга:")
    for i, item in enumerate(parsed_data, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   Автор: {item['author']}")
        print(f"   Рейтинг: {item['rating']}")
        print(f"   Комментарии: {item['comments']}")
        print(f"   Ссылка: {item['link']}")