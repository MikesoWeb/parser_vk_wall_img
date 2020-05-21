import requests, time
from config import owner_id, client_secret, v_api

url_api = 'https://api.vk.com/method/wall.get'
count = 100
offset = 0
count_posts = 0
count_img = 0

while offset <= count:
    response = requests.get(url_api, params={
        'v':v_api,
        'owner_id': owner_id,
        'access_token':client_secret,
        'count': count,
        'offset': offset
    })

    array_posts = response.json()['response']['items']
    time.sleep(0.2)
    offset += count


    for i in array_posts:

        for j in range(10):
            try:
                if i['attachments'][j]['type'] == 'photo':
                    count_img += 1
                    print(i['attachments'][j]['photo']['sizes'][-1]['url'])
                else:
                    pass
            except:
                pass
        count_posts += 1

print()
print('Всего изображений в выбраных постах: ', count_img)
print('Всего постов: ', count_posts- count)