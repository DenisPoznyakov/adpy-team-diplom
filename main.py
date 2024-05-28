from random import randrange

from vk_api.longpoll import VkEventType

from db.models import UserVK, FavoriteVK
from db.db_functions import (create_tables, add_user, add_or_del_favorite, add_blacklist,
                             check_user_in_blacklist, get_favorites, check_user_in_favorites)
from api.api_functions import find_user, get_user_name, get_city, get_age, get_user_photos
from api.api import vk, longpoll, keyboard


if __name__ == '__main__':
    create_tables()

    def write_msg(us_id, msg):
        """метод отправки сообщений"""
        vk.method('messages.send', {'user_id': us_id,
                                    'message': msg,
                                    'random_id': randrange(10 ** 7),
                                    'keyboard': keyboard.get_keyboard(),
                                    'attachment': ','.join(attachments)})

    next_user = None  # переменная для генератора

    for event in longpoll.listen():  # Основной цикл
        if event.type == VkEventType.MESSAGE_NEW:  # Если пришло новое сообщение

            if event.to_me:  # Если оно имеет метку для меня( то есть бота)
                request = event.text  # Сообщение от пользователя
                user_id = event.user_id  # id пользователя
                attachments = []  # список для фото

                if not next_user:  # если генератора еще нет, создаем новый
                    next_user = find_user(user_id)

                if request.lower() in ("привет", "старт"):
                    # получаем данные для объекта user(вообще в бд можно хранить только id, остальное лишняя информация, но пусть будет раз уже написали)
                    first_name, last_name = get_user_name(user_id)
                    city = get_city(user_id)[1]
                    age = get_age(user_id)
                    user = UserVK(user_id=user_id, first_name=first_name, last_name=last_name, city=city, age=age)  # создаем объект user
                    add_user(user)  # добавляем в бд

                    write_msg(user_id, f"{first_name} {last_name}, добро пожаловать в бота для знакомств.\n"
                                       f"Нажимайте '>>>>>>' для пролистывания предложений для знакомств.")

                elif request == "»&gt;":  # кнопка для следующего предложения
                    try:  # проверяем, есть ли следующий пользователь
                        tmp_user = next_user.__next__()

                        tmp_id = tmp_user[0]
                        tmp_first_name = tmp_user[1]
                        tmp_last_name = tmp_user[2]
                        tmp_link = tmp_user[3]
                        tmp_message = f'{tmp_first_name} {tmp_last_name}\nссылка {tmp_link}'

                        if not check_user_in_blacklist(user_id, tmp_id):  # проверяем, нет ли пользователя в черном списке
                            attachments = get_user_photos(tmp_id)  # формируем список фото
                            write_msg(user_id, tmp_message)
                        else:
                            write_msg(user_id, f'{tmp_first_name} {tmp_last_name} у Вас в черном списке.')

                    except StopIteration:  # если список закончился
                        write_msg(user_id, "Вы пролистали весь список.\nЧтобы начать заново нажмите: 'Начать сначала.'")

                elif request == 'Начать сначала':
                    next_user = find_user(user_id)  # создаем заново генератор
                    message = "Нажимайте '>>>>>>' для пролистывания предложений для знакомств."
                    try:
                        del tmp_id  # удаляем временную переменную, если она есть
                        write_msg(user_id, message)
                    except NameError:
                        write_msg(user_id, message)

                elif request == "Добавить в избранные":
                    try:
                        if not check_user_in_blacklist(user_id, tmp_id):  # если пользователя нет в черном списке
                            favorite = FavoriteVK(user_id=tmp_id, first_name=tmp_first_name,
                                                last_name=tmp_last_name, link=tmp_link)  # создаем объект избранного
                            add_or_del_favorite(user, favorite)  # добавляем в бд
                            write_msg(user_id, "Предложение добавленно/удалено в Ваш список изранных.")
                        else:
                            write_msg(user_id, f'{tmp_first_name} {tmp_last_name} у Вас в черном списке.')
                    except NameError:
                        write_msg(user_id, "У Вас еще нет предложений. Нажмите '>>>>>>'")

                elif request == "Избранные":
                    message_list = get_favorites(user)
                    if message_list:
                        for i, message in enumerate(message_list):
                            write_msg(user_id, f'{i+1} - {message}')
                    else:
                        write_msg(user_id, 'Ваш список избранных пуст.')

                elif request == "Добавить в черный список":
                    try:
                        if not check_user_in_favorites(user_id, tmp_id):  # если пользователя нет в избранных
                            add_blacklist(user, tmp_id)
                            write_msg(user_id, "Предложение добавленно в черный список.")
                        else:
                            write_msg(user_id, "Данный пользователь у Вас в избранных, сначала удалите его из избранных.")
                    except NameError:
                        write_msg(user_id, "У Вас еще нет предложений. Нажмите '>>>>>>'")

                elif request.lower() == "пока":
                    write_msg(event.user_id, "Пока((")

                else:
                    write_msg(event.user_id, "Не понял вашего ответа...")
