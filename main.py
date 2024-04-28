import json
import time
import re

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

import arz_apii
import requests
import vk_api

from const import GOOGLE_SHEETS_URL, VK_API_KEY, GROUP_ID, DB_HOST, DB_LOGIN, DB_PASS, DB_NAME
from controllers.MySQLController import DatabaseController
from controllers.SeleniumController import SeleniumController

# controller = SeleniumController() # Создание экземпляра класса SeleniumController
# cookies = controller.login_forum() # Авторизация на форуме и получение cookies
# api = arz_apii.ArizonaAPI(user_agent="your", cookie=cookies)
#
# user = api.current_member
# print(f'Успешно авторизовались!\nИмя пользователя: {user.username} | Звание: {user.user_title}\nАватарка: {user.avatar}\nСообщений: {user.messages_count} | Реакций: {user.reactions_count}\n')

db_controller = DatabaseController(host=DB_HOST,
                                   user=DB_LOGIN,
                                   password=DB_PASS,
                                   database=DB_NAME)

bh = vk_api.VkApi(token=VK_API_KEY)
give = bh.get_api()
longpoll = VkBotLongPoll(bh, group_id=GROUP_ID)

for event in longpoll.listen():
    if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.object.message['text']
            user_id = event.object.message['from_id']

            # Разбиваем сообщение на части для анализа команды
            parts = message.split()
            if len(parts) >= 3 and parts[0] == "!create_server" and user_id == 181922203:
                server_id = parts[1]
                name = ' '.join(parts[2:])  # Объединяем оставшиеся части в одну строку

                # Создание записи о сервере в базе данных
                db_controller.create_server_record(user_id, server_id, name)

                # Отправляем ответное сообщение о успешном создании записи
                give.messages.send(user_id=user_id, message="Запись о сервере успешно создана в базе данных.")




# page_number = input("Введите страницу с самой старой открытой темой: ")
# page_number = int(page_number)
# # Преобразование введенной строки в число
#
# while True:
#     threads = api.get_threads(1597, page_number)
#     page_have_open_threads = False
#
#     for i in threads["unpins"]:
#         thread = api.get_thread(i)
#         if thread.is_closed is False:
#             page_have_open_threads = True
#             print(f'{thread.id} | {thread.is_closed} | {thread.title} by {thread.creator.username}')
#             pattern = r'от\s*"?(\w+)"?'
#             match = re.search(pattern, thread.title)
#             nick = match.group(1)
#
#             params = {
#                 "nick": nick or "",
#                 "thread_number": thread.id or "",
#                 "content": thread.content or ""
#             }
#             response = requests.post(GOOGLE_SHEETS_URL, data=params)
#             if response.status_code == 200:
#                 print("Запись успешно сохранена в таблицу!")
#                 api.close_thread(thread.id)
#                 print("Закрыли тему")
#                 api.answer_thread(thread.id, "[CENTER][COLOR=rgb(247, 218, 100)]Добрый день уважаемый игрок![/COLOR]"
#                                            "<br><br>[COLOR=rgb(242, 162, 86)]Ваша заявка на амнистию рассматривается."
#                                            "<br>Результаты амнистии черного списка проекта и администрации будут опубликованы в общем списке 1 июня."
#                                            "<br>Результаты амнистии обычных нарушений будут публиковать в группе в ВК по мере проверки заявок, а так-же будут опубликованы в общем списке 1 июня."
#                                            "<br>Список можно будет найти в нашей группе вк [URL]https://vk.com/arizonagilbert16[/URL] , а так же в данном разделе амнистий."
#                                            "<br>Раньше публикации результаты узнать не возможно! Не нужно никому писать и переспрашивать. Приятной игры на нашем проекте.[/COLOR][/CENTER]")
#                 print("Ответили в теме")
#                 api.edit_thread_info(thread.id, thread.title, 17)
#                 print("Поменяли префикс темы")
#                 time.sleep(1)
#             else:
#                 print("Произошла ошибка при выполнении запроса:", response.status_code, response.content)
#                 print(f"{params['nick']} | {params['thread_number']} | {params['content']}")
#     if not page_have_open_threads:
#         break
