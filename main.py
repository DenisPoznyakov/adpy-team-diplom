# https://vk.com/club225855491
# в этом паблике я реализовал бота, напиши ему 'привет' и он отправит тебе в ответ фото, твой айди, имя, фамилию, город, код города, дату рождения и код пола.

from random import randrange
from pprint import pprint
import requests
import datetime

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# ключ доступа сообщества
token = 'vk1.a.Srf15C6wGCBcMObPuY6ZoKfAzAp57qt10wUIwtMyBAL-yXDYu41yoF7iQh1P6-LJVk4FiZS9YovCVpV4P0OirqDdxfcW8GP69dQHlVIkki127ir0be-jnQGzfgtHE5bhawiNWXZxChRsxpJqrbLtlL973c_YP8uPy0mq7KvFE2WLd0okWzKkLSyY7t5MAAuMRblfvFNA1k1snwWq8VjMBw'
# сервисный ключ доступа(приложения)
token_app = 'ddca84d2ddca84d2ddca84d2c0ded2c772dddcaddca84d2bbf5d222c3a66e248f563db7'
# ключь доступа пользователя
access_tocen = 'vk1.a.Uz2d8ZL06LRT-VZs4vVx2I06U8x9DugxYUwAf2L4XESHhlSEVj572sRBknvTNIMDgMxrJNKnKK3PQ8Q6MbPr8Y-MFnLlfzb30HE7Pv4L9dFUKj4Oy3-SFv9gC90GdxH6GYhz5PXTv4GjW_eaqqWx-pD4cSiFe_i9TB_sGblMcvFlE17MmwuD6IyfzalcJnZ7'

vk = vk_api.VkApi(token=token) # Авторизуемся как сообщество
vk_app = vk_api.VkApi(token=token_app) # авторизируемся как приложение
longpoll = VkLongPoll(vk) # Работа с сообщениями

# scope отвечает за доступ к контенту, если работаь не будет, смотри этот параметр
# без параметра scope = offline, для этого должно быть стенделон приложение
# https://oauth.vk.com/authorize?client_id=51921824&display=mobile&redirect_uri=https://oauth.vk.com/blank.html&scope=offline&response_type=token&v=5.199&state=123456
# access_token=vk1.a.Uz2d8ZL06LRT-VZs4vVx2I06U8x9DugxYUwAf2L4XESHhlSEVj572sRBknvTNIMDgMxrJNKnKK3PQ8Q6MbPr8Y-MFnLlfzb30HE7Pv4L9dFUKj4Oy3-SFv9gC90GdxH6GYhz5PXTv4GjW_eaqqWx-pD4cSiFe_i9TB_sGblMcvFlE17MmwuD6IyfzalcJnZ7

def write_msg(user_id, message):
    """метод отправки сообщений"""
    vk.method('messages.send', {'user_id': user_id,
                                     'message': message,
                                     'random_id': randrange(10 ** 7)})

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
        find_sex = 2
        return find_sex
    elif sex == 2:
        find_sex = 1
        return find_sex

def get_city(user_id):
    """получение кода и названия города"""
    getting_api = vk.get_api()
    info = getting_api.users.get(user_ids=user_id, fields='city')[0]
    city_title = info['city']['title']
    city_id = str(info['city']['id'])
    info_city = [city_id, city_title]
    return info_city

def get_age(user_id):
    """получение возраста пользователя и уставка границ для поиска +-1 год"""
    getting_api = vk.get_api()
    info = getting_api.users.get(user_ids=user_id, fields='bdate')[0]
    bdate = info['bdate']
    date_list = bdate.split('.')
    if len(date_list) == 3:
        year = int(date_list[2])
        year_now = int(datetime.date.today().year)
        age = year_now - year
        age_range = [age-1, age+1]
        return age_range
    elif len(date_list) == 2 or bdate not in info:
        write_msg(user_id, 'Введите год вашего рождения (в формате ГГГГ): ')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age = event.text
                age_range = [age - 1, age + 1]
                return age_range

def find_user(user_id):
    """поиск человека по полученным данным"""
    url = f'https://api.vk.com/method/users.search'
    params = {'access_token': access_tocen,
              'v': '5.199',
              'sex': find_sex(user_id),
              'age_from': get_age(user_id)[0],
              'age_to': get_age(user_id)[1],
              'city': get_city(user_id)[0],
              'fields': 'is_closed, id, first_name, last_name',
              'status': '1' or '6',
              'count': 500}
    resp = requests.get(url, params=params)
    resp_json = resp.json()
    dict_1 = resp_json['response']
    list_1 = dict_1['items']
    for person_dict in list_1:
        if person_dict.get('is_closed') == False:
            first_name = person_dict.get('first_name')
            last_name = person_dict.get('last_name')
            vk_id = str(person_dict.get('id'))
            vk_link = 'vk.com/id' + str(person_dict.get('id'))
            # теперь нужно внести полученные данные в бд
        else:
            continue

#     return resp_json
# pprint(find_user(151422792))

# функция получения данных фото в формате [[лайки, айди, ссылка][лайки, айди, ссылка][лайки, айди, ссылка]]
def get_user_photos(user_id):
    """получения данных фото"""
    # user_id = юзер_айди нужно вытаскивать из бд
    getting_api_app = vk_app.get_api()
    photo_info = getting_api_app.photos.get(owner_id=user_id, album_id='profile', extended=1) #получение json фотографий пользователя
    photos_likes_profile = []
    for photo in photo_info['items']:
        likes = photo['likes']['count']
        photo_id = photo['id']
        for i in photo['sizes']:
            link_list = []
            link_list.append(i['url'])
            link = link_list[-1]  # костыли с получением ссылки на фото
        photos_likes_profile.append([likes, photo_id, link])
    photos_likes_profile.sort()
    photos_likes_profile_best = [photos_likes_profile[-1], photos_likes_profile[-2],
                                     photos_likes_profile[-3]]
    return photos_likes_profile_best

def send_photo_1(user_id):
    """отправка первой фотографии"""
    vk.method('messages.send', {'user_id': user_id,
                                     'access_token': access_tocen,
                                     'attachment': f'photo{user_id}_{get_user_photos(user_id)[0][1]}',
                                     'random_id': 0})

def send_photo_2(user_id):
    """отправка второй фотографии"""
    vk.method('messages.send', {'user_id': user_id,
                                     'access_token': access_tocen,
                                     'attachment': f'photo{user_id}_{get_user_photos(user_id)[1][1]}',
                                     'random_id': 0})

def send_photo_3(user_id):
    """отправка третьей фотографии"""
    vk.method('messages.send', {'user_id': user_id,
                                     'access_token': access_tocen,
                                     'attachment': f'photo{user_id}_{get_user_photos(user_id)[2][1]}',
                                     'random_id': 0})



# Функция write_msg получает id пользователя ВК <user_id>, которому оно отправит сообщение и собственно само сообщение.
# здесь при передаче аргументов в 'attachment' подставляется идентификатор фотографии в формате 'photo{user_id}_{photo_id}'. в интеренетах говорят, что нужно передать список идентификаторов, но все-равно бот отправляет только одно фото. можешь побаловаться с этой штукой, поймешь о чем я
# def write_msg(user_id, message, photo_id):
#     photo_one = f'photo{user_id}_{photo_id}'
#     photo_two = 'photo151422792_333268754'
#     # photo151422792_333268754 моя фотка
#     # photo-57846937_457307562 фото мдк
#     vk.method('messages.send', {'user_id': user_id, 'message': message, "attachment": f'{photo_one}, {photo_two}', 'random_id': randrange(10 ** 7),})

 # функция для получения информации о пользователе с помощью vk_api
# def get_user_info(from_id):
#     #получение информации:
#     getting_api = vk.get_api()
#     info = getting_api.users.get(user_ids=from_id, fields='city, bdate, sex')[0]
#     city_title = info['city']['title']
#     city_id = str(info['city']['id'])
#     bdate = info['bdate']
#     sex = str(info['sex'])  # 1-женский, 2-мужской, 0-не указан
#
#     full_info = (
#             info.get('first_name') + ' '+
#             info['last_name'] + ' ' +
#             city_title + ' ' +
#             city_id + ' ' +
#             bdate + ' ' +
#             sex
#             )
#     return full_info




for event in longpoll.listen(): # Основной цикл
    if event.type == VkEventType.MESSAGE_NEW:  # Если пришло новое сообщение

        if event.to_me:  # Если оно имеет метку для меня( то есть бота)
            request = event.text # Сообщение от пользователя

            if request == "привет":
                # info = get_user_info(event.user_id)
                photo_id = get_user_photos(event.user_id)[0][1]
                write_msg(event.user_id, f"Хай, {get_user_name(event.user_id)[0]} {get_user_name(event.user_id)[1]} "
                                         f"{get_city(event.user_id)[0]} {get_city(event.user_id)[1]} "
                                         f"{find_sex(event.user_id)} "
                                         f"{get_age(event.user_id)[0]} {get_age(event.user_id)[1]}"
                                         f"{send_photo_1(event.user_id)}"
                                         f"{send_photo_2(event.user_id)}"
                                         f"{send_photo_3(event.user_id)}"
                          )
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")



# код клавиатуры я просто добавил, что бы потом с ним разобраться, клавиатура еще не работает в боте (это не втой код, это код из интеренетов)
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)

def sender(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0, keyboard=keyboard.get_keyboard())




# даже не помню что делает код ниже, он нахрен не нужон)))
# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#         if event.to_me:
#             print('New message:')
#             print(f'For me by: {event.user_id}', end='')
#
#             bot = VkBot(event.user_id)
#             write_msg(event.user_id, bot.new_message(event.text))
#
#             print('Text: ', event.text)
