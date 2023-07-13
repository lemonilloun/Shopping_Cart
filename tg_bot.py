import telebot
from telebot import types
from tg_token import token

def telegram_bot(token):
    bot = telebot.TeleBot(token)
    curr_cart_id = 0
    person = []
    global shop_list

    def cart_creation(message):
        person.append(message.text)
        bot.send_message(message.chat.id, f'Создание списка покупок для пользователя {person[-1]}')
        msg = bot.send_message(message.chat.id,
                         "Напишите ниже список покупок для пользователя.\n\nПришлите список в формате: \n<название продукта>-<стоимость> -<количество> ( по умолчанию количество равно 1)\n\nПример1: Молоко-67\nПример2: Хлеб-42-3",)
        bot.register_next_step_handler(msg, cart_packing)



    def cart_packing(message):
        #shop_list += message.text
        if message.text == "Завершить список покупок для пользователя":
            pass
        else:
            print(message.text)
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton("Завершить список покупок для пользователя"))
            msg = bot.send_message(message.chat.id, "Нажмите на кнопку для завершения списка", reply_markup=rmk)
            bot.register_next_step_handler(msg, cart_packing)



    @bot.message_handler(commands= ['shop', 'shopping'])
    def working(message):
        markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_create_cart = types.KeyboardButton("Создать")
        item_change_cart = types.KeyboardButton("Редактировать")
        markup_inline.add(item_create_cart, item_change_cart)
        msg = bot.send_message(message.chat.id, "Что бы вы хотели сделать c корзиной?",
                         reply_markup = markup_inline)
        bot.register_next_step_handler(msg, cart_answer)

    def cart_answer(message):
        if message.text == "Создать":
            msg = bot.send_message(message.chat.id, 'Напишите пользователя')
            bot.register_next_step_handler(msg, cart_creation)



    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Приветсвую тебя! Надеюсь я смогу помочь вам в организации покупок.")


    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

