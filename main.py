# https://vk.com/club225855491
# в этом паблике я реализовал бота, напиши ему 'привет' и он отправит тебе в ответ фото, твой айди, имя, фамилию, город, код города, дату рождения и код пола.

from random import randrange
from pprint import pprint

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# ключ доступа сообщества
token = 'vk1.a.Srf15C6wGCBcMObPuY6ZoKfAzAp57qt10wUIwtMyBAL-yXDYu41yoF7iQh1P6-LJVk4FiZS9YovCVpV4P0OirqDdxfcW8GP69dQHlVIkki127ir0be-jnQGzfgtHE5bhawiNWXZxChRsxpJqrbLtlL973c_YP8uPy0mq7KvFE2WLd0okWzKkLSyY7t5MAAuMRblfvFNA1k1snwWq8VjMBw'
# сервисный ключ доступа(приложения)
token_app = 'ddca84d2ddca84d2ddca84d2c0ded2c772dddcaddca84d2bbf5d222c3a66e248f563db7'

vk = vk_api.VkApi(token=token) # Авторизуемся как сообщество
vk_app = vk_api.VkApi(token=token_app) # авторизируемся как приложение
longpoll = VkLongPoll(vk) # Работа с сообщениями


# Функция write_msg получает id пользователя ВК <user_id>, которому оно отправит сообщение и собственно само сообщение.
# здесь при передаче аргументов в 'attachment' подставляется идентификатор фотографии в формате 'photo{user_id}_{photo_id}'. в интеренетах говорят, что нужно передать список идентификаторов, но все-равно бот отправляет только одно фото. можешь побаловаться с этой штукой, поймешь о чем я
def write_msg(user_id, message, photo_id):
    photo_one = f'photo{user_id}_{photo_id}'
    photo_two = 'photo151422792_333268754'
    # photo151422792_333268754 моя фотка
    # photo-57846937_457307562 фото мдк
    vk.method('messages.send', {'user_id': user_id, 'message': message, "attachment": f'{photo_one}, {photo_two}', 'random_id': randrange(10 ** 7),})

 # функция для получения информации о пользователе с помощью vk_api
def get_user_info(from_id):
    #получение информации:
    getting_api = vk.get_api()
    info = getting_api.users.get(user_ids=from_id, fields='city, bdate, sex')[0]
    city_title = info['city']['title']
    city_id = str(info['city']['id'])
    bdate = info['bdate']
    sex = str(info['sex'])  # 1-женский, 2-мужской, 0-не указан

    # поиск людей
    # search = getting_api.users.search(q='Денис Позняков')
    # pprint(search)

    full_info = (
            info.get('first_name') + ' '+
            info['last_name'] + ' ' +
            city_title + ' ' +
            city_id + ' ' +
            bdate + ' ' +
            sex
            )
    return full_info

# функция получения данных фото в формате [[лайки, айди, ссылка][лайки, айди, ссылка][лайки, айди, ссылка]]
def get_user_photos(from_id):

    getting_api_app = vk_app.get_api()
    photo_info = getting_api_app.photos.get(owner_id=from_id, album_id='profile', extended=1) #получение json фотографий пользователя
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


for event in longpoll.listen(): # Основной цикл
    if event.type == VkEventType.MESSAGE_NEW:  # Если пришло новое сообщение

        if event.to_me:  # Если оно имеет метку для меня( то есть бота)
            request = event.text # Сообщение от пользователя

            if request == "привет":
                info = get_user_info(event.user_id)
                photo_id = get_user_photos(event.user_id)[0][1]
                write_msg(event.user_id, f"Хай, {event.user_id} {info}", photo_id)
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
