# этот код я нашел на просторах интернета, он не рабочий, я просто из него черпал нужные строки

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = 'vk1.a.Srf15C6wGCBcMObPuY6ZoKfAzAp57qt10wUIwtMyBAL-yXDYu41yoF7iQh1P6-LJVk4FiZS9YovCVpV4P0OirqDdxfcW8GP69dQHlVIkki127ir0be-jnQGzfgtHE5bhawiNWXZxChRsxpJqrbLtlL973c_YP8uPy0mq7KvFE2WLd0okWzKkLSyY7t5MAAuMRblfvFNA1k1snwWq8VjMBw'
vk = vk_api.VkApi(token=token) # Авторизуемся как сообщество
longpoll = VkLongPoll(vk) # Работа с сообщениями

class VkBot:

    def __init__(self, user_id):
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА"]

    def _get_user_name_from_vk_id(self, user_id):
        # vk = vk_session.get_api()
        # id = "1"
        # user_get = vk.users.get(user_ids=(id))
        # user_get = user_get[0]
        first_name = user_id.get['first_name']
        last_name = user_id.get['last_name']
        full_name = first_name + " " + last_name
        return first_name




        # request = requests.get("https://vk.com/id" + str(user_id))
        # bs = bs4.BeautifulSoup(request.text, "html.parser")
        #
        # user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        #
        # return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        else:
            return "Не понимаю о чем вы..."