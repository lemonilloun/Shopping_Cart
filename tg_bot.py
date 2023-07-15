import telebot
import json
from telebot import types
from tg_token import token
from cart_shop import writting

class Cart(object):
    cart_list = {}
    cart_id = 0

    def add_cart_id(self, cart_id):
        self.cart_id = cart_id

    def add_chat_id(self, chat_id):
        self.chat_id = chat_id

    def add_person(self, person, shop_list):
        self.cart_list[str(person)] = ""

    def add_list_of_products(self, person, shop_list):
        if person in self.cart_list:
            x = self.cart_list[person]
            self.cart_list[person] = x + shop_list
        else:
            self.cart_list[person] = shop_list

    def clear(self):
        self.cart_id = 0
        self.chat_id = 0
        self.cart_list = {}

    def get_info(self):
        res = {"chat_id":self.chat_id, "cart_id":self.cart_id, "persons" : {per:lst for (per, lst) in self.cart_list.items()}}
        return res

    def get_catr_id(self):
        return self.cart_id

    def get_cart_list(self):
        return self.cart_list


def telegram_bot(token):
    bot = telebot.TeleBot(token)
    person = []
    cart = Cart()

    def cart_creation(message):
        person.append(message.text)
        bot.send_message(message.chat.id, f'Создание списка покупок для пользователя {person[-1]}')
        msg = bot.send_message(message.chat.id,
                         "Напишите ниже список покупок для пользователя.\n\nПришлите список в формате: \n<название продукта>-<стоимость> -<количество> ( по умолчанию количество равно 1)\n\nПример1: Молоко-67\nПример2: Хлеб-42-3",)
        bot.register_next_step_handler(msg, cart_packing)



    def cart_packing(message):
        if message.text == "Завершить список покупок для пользователя":
            print(cart.get_info())
        else:
            shop_list = message.text + "\n"
            cart.add_list_of_products(person[-1], shop_list)
            print(person[-1])
            print(shop_list)
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton("Завершить список покупок для пользователя"))
            msg = bot.send_message(message.chat.id, "Нажмите на кнопку для завершения списка", reply_markup=rmk)
            bot.register_next_step_handler(msg, cart_packing)



    @bot.message_handler(commands= ['shop', 'shopping'])
    def working(message):
        person.clear()
        markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_create_cart = types.KeyboardButton("Создать")
        item_change_cart = types.KeyboardButton("Редактировать")
        markup_inline.add(item_create_cart, item_change_cart)
        msg = bot.send_message(message.chat.id, "Что бы вы хотели сделать c корзиной?",
                         reply_markup = markup_inline)
        bot.register_next_step_handler(msg, cart_answer)

    def cart_answer(message):
        if message.text == "Создать":
            f = open("curr_cart_num.txt", 'r+')
            num = [int(x) for x in f][-1] + 1
            f.write(str(num) + "\n")
            f.close()
            cart.clear()
            cart.add_chat_id(message.chat.id)
            cart.add_cart_id(num)
            msg = bot.send_message(message.chat.id, 'Напишите пользователя')
            bot.register_next_step_handler(msg, cart_creation)



    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Приветсвую тебя! Надеюсь я смогу помочь вам в организации покупок.\nДля начала работы пропишите в чате /shop или /shopping")


    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

