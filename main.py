from sys import getsizeof
from uuid import uuid4

import os
import requests
import sys
import time

from utils import timer, write_url_to_txt, save_image_posts, get_from_env


def get_image_100_posts(count=10):
    """ Авторизуемся и получаем изображения с указанных в массиве постов """
    token = get_from_env('VK_TOKEN')
    owner = get_from_env('OWNER_ID')
    api = get_from_env('V_API')

    try:
        os.environ['VK_TOKEN'] and os.environ['OWNER_ID'] and os.environ['V_API']
    except KeyError:
        print()
        print('Внимание! Проверьте переменные окружения')
        print('Работа программы прекращена!')
        sys.exit(1)

    url_api = 'https://api.vk.com/method/wall.get'
    count = count
    offset = 0

    while offset <= count:
        response = requests.get(url_api, params={
            'v': api,
            'owner_id': owner,
            'access_token': token,
            'count': count,
            'offset': offset
        })

        # Собираем список items каждого поста
        array_posts = response.json()['response']['items']
        offset += count
        return array_posts


@timer
def get_url_images():
    """Итерируемся в пришедшем массиве с данными и ищем там ссылки на изображения в постах"""
    count_posts, count_img = 0, 0
    array_posts = get_image_100_posts()
    # print('ARRAY', array_posts)
    for i in array_posts:
        # идем по массиву items каждого поста
        # 10 это каждое вложение в посту / attachment
        for attachment in range(10):
            time.sleep(0.02)
            try:
                if i['attachments'][attachment]['type'] == 'photo':
                    count_img += 1
                    # Записываем ссылки в текстовый файл
                    one_url = i['attachments'][attachment]['photo']['sizes'][-1]['url']
                    write_url_to_txt(one_url)
                    save_image_posts(one_url, (str(uuid4()) + '.png'))
            except IndexError:
                ...
        count_posts += 1

    print()
    print('Всего изображений в выбранных постах: ', count_img)
    print('Всего постов: ', count_posts)
    print('Размер списка с данными', getsizeof(array_posts))
    print('Размер кортежа с данными', getsizeof(tuple(array_posts)))


if __name__ == '__main__':
    get_url_images()
