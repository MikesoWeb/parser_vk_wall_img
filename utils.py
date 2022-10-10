import time, os
import requests
from dotenv import load_dotenv


def get_from_env(key):
    load_dotenv()
    return os.getenv(key)


def timer(func):
    def wrapper():
        start_time = time.time()
        print('Декоратор начал замер времени выполнения функции')
        func()
        end_time = time.time() - start_time
        print('Работа окончена. ', 'Время выполнения функции: ', round(end_time, 3), 'секунд')

    return wrapper


def write_url_to_txt(one_url):
    "Получаем ссылку на изображение и записываем ее в текстовый файл"
    with open('urls_posts.txt', 'a', encoding='utf-8') as file:
        file.write(one_url),
        file.write('\n')


def save_image_posts(url, filename):
    url = url
    response = requests.get(url)

    with open('PHOTO_WALL/' + filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
        time.sleep(0.2)
