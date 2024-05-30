from random import randrange

from vk_api.longpoll import VkEventType

from db.models import UserVK, FavoriteVK
from db.db_functions import (create_tables, add_user, add_or_del_favorite, add_blacklist,
                             check_user_in_blacklist, get_favorites, check_user_in_favorites, del_user)
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

    next_user_dict = {}
    flag = True

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            request = event.text
            user_id = event.user_id
            attachments = []

            if request.lower() in ("привет", "старт"):
                flag = False
                if user_id not in next_user_dict:
                    next_user_dict[user_id] = find_user(user_id)

                next_user = next_user_dict[user_id]

                first_name, last_name = get_user_name(user_id)
                city = get_city(user_id)[1]
                age = get_age(user_id)
                user = UserVK(user_id=user_id, first_name=first_name, last_name=last_name, city=city, age=age)
                add_user(user)

                write_msg(user_id, f"{first_name} {last_name}, добро пожаловать в бота для знакомств.\n"
                                   f"Нажимайте '>>>>>>' для пролистывания предложений для знакомств.")

            elif request == "»&gt;":
                if not flag:
                    try:
                        tmp_user = next_user.__next__()

                        tmp_id = tmp_user[0]
                        tmp_first_name = tmp_user[1]
                        tmp_last_name = tmp_user[2]
                        tmp_link = tmp_user[3]
                        tmp_message = f'{tmp_first_name} {tmp_last_name}\nссылка {tmp_link}'

                        if not check_user_in_blacklist(user_id, tmp_id):
                            attachments = get_user_photos(tmp_id)
                            write_msg(user_id, tmp_message)
                        else:
                            write_msg(user_id, f'{tmp_first_name} {tmp_last_name} у Вас в черном списке.')

                    except StopIteration:
                        write_msg(user_id, "Вы пролистали весь список.\nЧтобы начать заново нажмите: 'Начать сначала.'")
                else:
                    write_msg(event.user_id, "Введите 'привет' или 'старт'.")

            elif request == 'Начать сначала':
                if not flag:
                    next_user_dict[user_id] = find_user(user_id)
                    next_user = next_user_dict[user_id]

                    message = "Нажимайте '>>>>>>' для пролистывания предложений для знакомств."
                    try:
                        del tmp_id
                        write_msg(user_id, message)
                    except NameError:
                        write_msg(user_id, message)
                else:
                    write_msg(event.user_id, "Введите 'привет' или 'старт'.")

            elif request == "Добавить в избранные":
                if not flag:
                    try:
                        if not check_user_in_blacklist(user_id, tmp_id):
                            favorite = FavoriteVK(user_id=tmp_id, first_name=tmp_first_name,
                                                last_name=tmp_last_name, link=tmp_link)
                            add_or_del_favorite(user, favorite)
                            write_msg(user_id, "Предложение добавленно/удалено в Ваш список изранных.")
                        else:
                            write_msg(user_id, f'{tmp_first_name} {tmp_last_name} у Вас в черном списке.')
                    except NameError:
                        write_msg(user_id, "У Вас еще нет предложений. Нажмите '>>>>>>'")
                else:
                    write_msg(event.user_id, "Введите 'привет' или 'старт'.")

            elif request == "Избранные":
                if not flag:
                    message_list = get_favorites(user)
                    if message_list:
                        for i, message in enumerate(message_list):
                            write_msg(user_id, f'{i+1} - {message}')
                    else:
                        write_msg(user_id, 'Ваш список избранных пуст.')
                else:
                    write_msg(event.user_id, "Введите 'привет' или 'старт'.")

            elif request == "Добавить в черный список":
                if not flag:
                    try:
                        if not check_user_in_favorites(user_id, tmp_id):
                            add_blacklist(user, tmp_id)
                            write_msg(user_id, "Предложение добавленно в черный список.")
                        else:
                            write_msg(user_id, "Данный пользователь у Вас в избранных, "
                                               "сначала удалите его из избранных.")
                    except NameError:
                        write_msg(user_id, "У Вас еще нет предложений. Нажмите '>>>>>>'")
                else:
                    write_msg(event.user_id, "Введите 'привет' или 'старт'.")

            elif request.lower() == "пока":
                if not flag:
                    flag = True
                    del next_user_dict[user_id]
                    del next_user
                    del_user(user_id)
                    write_msg(event.user_id, "Пока((. Если хотите начать заново, введите 'привет' или 'старт'.")
                else:
                    write_msg(event.user_id, "Введите 'привет' или 'старт'.")

            else:
                write_msg(event.user_id, "Не понял вашего ответа...")
