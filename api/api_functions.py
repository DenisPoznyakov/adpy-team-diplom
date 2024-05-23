import datetime

import requests

from api.api import vk, vk_app
from tokens import access_token


def get_user_name(user_id):
    """получение имени пользователя"""
    getting_api = vk.get_api()
    info = getting_api.users.get(user_ids=user_id)[0]
    first_name = info.get('first_name')
    last_name = info['last_name']
    full_name = [first_name, last_name]
    return full_name


def find_sex(user_id):
    """получения пола и замены его на противоположный"""
    getting_api = vk.get_api()
    info = getting_api.users.get(user_ids=user_id, fields='sex')[0]
    sex = int(info['sex'])  # 1-женский, 2-мужской, 0-не указан
    if sex == 1:
        return 2
    elif sex == 2:
        return 1


def get_city(user_id):
    """получение кода и названия города"""
    getting_api = vk.get_api()
    info = getting_api.users.get(user_ids=user_id, fields='city')[0]
    city_title = info['city']['title']
    city_id = str(info['city']['id'])
    info_city = [city_id, city_title]
    return info_city


def get_age(user_id):
    """получение возраста пользователя, если не в правильном формате или не указан, то берется 25 лет"""
    getting_api = vk.get_api()
    info = getting_api.users.get(user_ids=user_id, fields='bdate')[0]
    bdate = info['bdate']
    date_list = bdate.split('.')
    if len(date_list) == 3:
        year = int(date_list[2])
        year_now = int(datetime.date.today().year)
        age = year_now - year
        return age
    elif len(date_list) == 2 or bdate not in info:
        age = 25
        return age


def find_user(user_id):
    """Генератор поиска по полученным данным"""
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': access_token,
              'v': '5.199',
              'sex': find_sex(user_id),
              'age_from': get_age(user_id) - 1,
              'age_to': get_age(user_id) + 1,
              'city': get_city(user_id)[0],
              'fields': 'is_closed, id, first_name, last_name',
              'status': '1' or '6',
              'count': 500}
    resp = requests.get(url, params=params)
    resp_json = resp.json()
    items_list = resp_json['response']['items']

    for item in items_list:
        if not item.get('is_closed'):
            item_id = item.get('id')
            item_first_name = item.get('first_name')
            item_last_name = item.get('last_name')
            item_link = 'vk.com/id' + str(item_id)
            yield item_id, item_first_name, item_last_name, item_link
        else:
            continue


def get_user_photos(user_id):
    getting_api_app = vk_app.get_api()
    photo_info = getting_api_app.photos.get(owner_id=user_id, album_id='profile', extended=1)
    count_photo = photo_info['count'] # количество фото у пользователя
    photos_likes_profile = []
    if count_photo >= 3: # если фото больше или равно 3
        tmp_list = []
        for item in photo_info['items']:
            likes = item['likes']['count'] # кол-во лайков
            photo_id = item['id'] # id фото
            tmp_list.append([likes, photo_id])
        tmp_list.sort(reverse=True)
        for elem in tmp_list[:3]:
            photos_likes_profile.append(f'photo{user_id}_{elem[1]}')
        return photos_likes_profile

    else: # если фото меньше 3
        for item in photo_info['items']:
            photo_id = item['id']  # id фото
            photos_likes_profile.append(f'photo{user_id}_{photo_id}')
        return photos_likes_profile
