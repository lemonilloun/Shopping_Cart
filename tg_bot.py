import telebot
from telebot import types
from tg_token import token
def telegram_bot(token):
    bot = telebot.TeleBot(token)
    @bot.message_handler(commands= ['shop', 'shopping'])
    def working(message):
        markup_inline = types.InlineKeyboardMarkup()
        item_create_cart = types.InlineKeyboardButton(text="Создать",
                                               callback_data = 'create')
        item_change_cart = types.InlineKeyboardButton(text = "Редактировать",
                                                      callback_data = 'change')

        markup_inline.add(item_create_cart, item_change_cart)
        bot.send_message(message.chat.id, "Что бы вы хотели сделать c корзиной?",
                         reply_markup = markup_inline)

    @bot.callback_query_handler(func=lambda call: True)
    def answer(call):
        if call.data.lower() == 'create':
            bot.send_message(call.message.chat.id, "Ща")
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Приветсвую тебя!")
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "давай":
            bot.send_message(message.chat.id, "ну выбирай давай")
        else:
            bot.send_message(message.chat.id, "че говоришь?")


    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

