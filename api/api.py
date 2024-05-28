import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from tokens import token, token_app


vk = vk_api.VkApi(token=token)  # Авторизуемся как сообщество
vk_app = vk_api.VkApi(token=token_app)  # авторизируемся как приложение
longpoll = VkLongPoll(vk)  # Работа с сообщениями
keyboard = VkKeyboard(one_time=False)

keyboard.add_button('Начать сначала', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('>>>', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Добавить в избранные', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Избранные', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Добавить в черный список', color=VkKeyboardColor.NEGATIVE)
