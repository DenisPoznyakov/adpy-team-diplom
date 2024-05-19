from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from models import UserVK, FavoriteVK, BlacklistVK
from my_functions import create_tables, add_user, add_or_del_favorite, add_or_del_blacklist, check_user_in_blacklist, get_favorites


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

keyboard.add_button('Старт', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('<<<', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('>>>', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Добавить в избранные', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Избранные', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Добавить в черный список', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Черный список', color=VkKeyboardColor.SECONDARY)


if __name__ == '__main__':
    create_tables()

    user1 = UserVK(user_id=10, first_name='Вася', last_name='Пупкин', city='Москва', age=25, gender='м')
    user2 = UserVK(user_id=11, first_name='Мишка', last_name='Япончик', city='Одесса', age=30, gender='м')
    user3 = UserVK(user_id=12, first_name='Маруся', last_name='Климова', city='Комсомольск-на-Амуре', age=20,
                   gender='ж')
    user4 = UserVK(user_id=13, first_name='Эдуард', last_name='Пистолетов', city='Сочи', age=35, gender='м')

    favorite1 = FavoriteVK(user_id=14, first_name='Джеки', last_name='Чан', link='raratayqha.ru')
    favorite2 = FavoriteVK(user_id=15, first_name='Жан-Клод', last_name='Ван-Дам', link='kcgue.ru')
    favorite3 = FavoriteVK(user_id=16, first_name='Майкл', last_name='Дудиков', link='akoeemolo.ru')
    favorite4 = FavoriteVK(user_id=17, first_name='Сильвестр', last_name='Сталлоне', link='poejdeydc.ru')
    favorite5 = FavoriteVK(user_id=18, first_name='Майкл', last_name='Джордан', link='xnioq.ru')

    blacklist1 = BlacklistVK(user_id=19)
    blacklist2 = BlacklistVK(user_id=20)
    blacklist3 = BlacklistVK(user_id=21)
    blacklist4 = BlacklistVK(user_id=22)

    add_user(user1)
    add_user(user2)
    add_user(user1)
    add_user(user2)
    add_user(user4)
    add_user(user3)

    add_or_del_favorite(user1, favorite1)
    add_or_del_favorite(user1, favorite2)
    add_or_del_favorite(user1, favorite3)
    add_or_del_favorite(user2, favorite3)
    add_or_del_favorite(user3, favorite2)
    # add_or_del_favorite(user1, favorite1)

    add_or_del_blacklist(user1, blacklist2)
    add_or_del_blacklist(user2, blacklist2)
    add_or_del_blacklist(user4, blacklist3)
    add_or_del_blacklist(user4, blacklist1)
    add_or_del_blacklist(user1, blacklist2)

    print(check_user_in_blacklist(user1, blacklist2))
    print(check_user_in_blacklist(user2, blacklist2))
    print(check_user_in_blacklist(user4, blacklist3))
    print(check_user_in_blacklist(user3, blacklist3))

    favorite_list1 = get_favorites(user1)
    favorite_list2 = get_favorites(user2)
    for favorite in favorite_list1:
        print(favorite)
    for favorite in favorite_list2:
        print(favorite)

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
