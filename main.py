import os
import telepot
from telepot.loop import MessageLoop
from pprint import pprint

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

bot = telepot.Bot(os.environ['TOKEN'])
print(bot.getMe())

q = [("Вопрос 1", ("Ответ 1", "Ответ 2", "Правильный ответ", "Ответ 4"), 3),
     ("Вопрос 2", ("Ответ 1", "Правильный ответ", "Ответ 3", "Ответ 4"), 2),
     ("Вопрос 3", ("Ответ 1", "Ответ 2", "Ответ 3", "Правильный ответ"), 4)]

data = {}
correct = {}


def question(user, chat_id):
    num = data.get(user, -1) + 1
    bot.sendMessage(chat_id,
                    q[num][0],
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text=q[num][1][0],
                                                 callback_data='/answer 1'),
                            InlineKeyboardButton(text=q[num][1][1],
                                                 callback_data='/answer 2')
                        ],
                        [
                            InlineKeyboardButton(text=q[num][1][2],
                                                 callback_data='/answer 3'),
                            InlineKeyboardButton(text=q[num][1][3],
                                                 callback_data='/answer 4')
                        ]
                    ]))

    data[user] = num


def get_answer(user):
    return q[data[user]][2]


def handle(msg):
    user = msg["from"]["id"]
    if "chat" in msg.keys():
        chat_id = msg["chat"]["id"]
        if msg["text"] == "/start" or msg["text"] == "Заново":
            correct[user] = 0
            data[user] = -1
            bot.sendMessage(
                chat_id,
                'Этот проект создан для определения уровня учеников поступающих на курс.',
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="И такую клавиатуру")]]))

            bot.sendMessage(
                chat_id,
                'За этот проект я узнал как делать',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="такую", callback_data='/aa')
                ]]))

            bot.sendMessage(
                chat_id,
                '.\n\n(P.S я уже раньше работал с telepot и Python)\n(P.P.S я искал информацию про InlineKeyboard на stackoverflow.com)\n\n.'
            )

            bot.sendMessage(chat_id, 'Здравствуйте!')
            question(user, chat_id)

        if msg["text"] == "Выход":
            bot.sendMessage(chat_id,
                            'До свидания!',
                            reply_markup=ReplyKeyboardRemove())
        if user not in data.keys():
            bot.sendMessage(chat_id, 'Напишите /start')
    elif "data" in msg.keys():
        chat_id = msg["message"]["chat"]["id"]
        if msg["data"] in ["/answer 1", "/answer 2", "/answer 3", "/answer 4"]:
            answer = int(msg["data"][-1])
            if answer == get_answer(user):
                correct[user] = correct.get(user, 0) + 1
            print(correct)
            if data[user] == len(q) - 1:
                bot.sendMessage(chat_id, 'Это был последний вопрос')
                bot.sendMessage(chat_id,
                                'Ваш результат: ' + str(correct[user]) + "/" +
                                str(len(q)),
                                reply_markup=ReplyKeyboardMarkup(keyboard=[[
                                    KeyboardButton(text="Выход"),
                                    KeyboardButton(text="Заново")
                                ]]))
            else:
                question(user, chat_id)


MessageLoop(bot, handle).run_as_thread()
while True:
    pass
