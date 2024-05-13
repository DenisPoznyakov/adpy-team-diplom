from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, User, Favorites, UserFavorites, Photos, BlackList, UserBlackList


driver_db = input('Введите название СУБД: ')
login = input('Введите имя пользователя: ')
password = input('Введите пароль: ')
host = input('Введите host сервера: ')
port = input('Введите порт сервера: ')
name_db = input('Введите название БД: ')


DSN = f'{driver_db}://{login}:{password}@{host}:{port}/{name_db}'

engine = sqlalchemy.create_engine(DSN)

session = sessionmaker(bind=engine)()

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
keyboard = VkKeyboard(one_time=False)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'random_id': randrange(10 ** 7),
                                'keyboard': keyboard.get_keyboard()
                                })


keyboard.add_button('<<<', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('>>>', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Добавить в избранные', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Избранные', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Добавить в черный список', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Черный список', color=VkKeyboardColor.SECONDARY)


if __name__ == '__main__':
    create_tables(engine)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет":
                    write_msg(event.user_id, f"Хай, {event.user_id}")
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")
