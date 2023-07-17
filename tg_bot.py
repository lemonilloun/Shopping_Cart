import telebot
import json
from telebot import types
from tg_token import token
from cart_shop import writting

class Cart(object):
    cart_list = {}
    cart_id = 0
    curr_work_id = -1
    split_prod_list = {}
    splt_persons = []
    split_list = "" #обновляемое значение

    def set_splt_persons(self, pers):
        if pers == "0":
            self.splt_persons.clear()
        elif pers not in self.splt_persons:
            self.splt_persons.append(pers)

    def get_splt_persons(self):
        return self.splt_persons
    def set_split_list(self, lst):
        self.split_list = lst

    def get_splt_list(self):
        return self.split_list

    def set_work_id(self, new_id):
        self.curr_work_id = new_id

    def get_work_id(self):
        return self.curr_work_id
    def add_cart_id(self, cart_id):
        self.cart_id = cart_id

    def add_chat_id(self, chat_id):
        self.chat_id = chat_id

    def add_person(self, person, shop_list):
        if str(person) in self.cart_list:
            self.cart_list[str(person)] += shop_list
        else:
            self.cart_list[str(person)] = shop_list

    def add_list_of_products(self, person, shop_list):
        if person in self.cart_list:
            x = self.cart_list[person]
            self.cart_list[person] = x + shop_list
        else:
            self.cart_list[person] = shop_list

    def clear_list_for_person(self, person):
        if person in self.cart_list:
            self.cart_list[person] = ""

    def split_product(self, shop_list, persons):
        self.split_prod_list[shop_list] = persons

    def get_split_product(self):
        return self.split_prod_list

    def clear(self):
        self.cart_id = 0
        self.chat_id = 0
        self.cart_list = {}
        self.curr_work_id = -1
        self.split_list = ""
        self.splt_persons.clear()
        self.split_prod_list = {}

    def get_info(self):
        res = {"chat_id":self.chat_id, "cart_id":self.cart_id, "persons" : {per:lst for (per, lst) in self.cart_list.items()},
               "splits" : {prod:per for (prod, per) in self.split_prod_list.items()}}
        return res

    def get_catr_id(self):
        return self.cart_id

    def get_cart_list(self):
        return self.cart_list


def telegram_bot(token):
    bot = telebot.TeleBot(token)
    person = []
    #splt_persons = []
    cart = Cart()


    def cart_creation(message):
        person.append(message.text)
        bot.send_message(message.chat.id, f'Создание списка покупок для пользователя {person[cart.get_work_id()]}')
        msg = bot.send_message(message.chat.id,
                         "Напишите ниже список покупок для пользователя.\n\nПришлите список в формате: \n<название продукта>-<цена> -<количество> ( по умолчанию количество равно 1)\n\nПример1: Молоко-67\nПример2: Хлеб-42-3")
        bot.register_next_step_handler(msg, cart_packing)


    def cart_editing(message):
        cart.set_work_id(person.index(message.text))
        cart.clear_list_for_person(person[cart.get_work_id()])
        bot.send_message(message.chat.id, f'Изменение списка покупок для пользователя {person[cart.get_work_id()]}')
        msg = bot.send_message(message.chat.id, "Пожалуйста перепишите список для пользователя в формате: \n<название продукта>-<стоимость> -<количество> ( по умолчанию количество равно 1)\n\nПример1: Молоко-67\nПример2: Хлеб-42-3",
                               reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, cart_packing)


    def cart_processing(message):
        if message.text == "Добавить пользователя":
            msg = bot.send_message(message.chat.id, "Напишите нового пользователя", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, cart_creation)
        elif message.text == "Вывести итоговый чек":
            res = writting(cart.get_info())
            print(cart.get_info())
            bot.send_message(message.chat.id, res)
            person.clear()
            cart.set_work_id(-1)
            bot.send_message(message.chat.id, "Приятных покупок!\nДля создания новой корзины пропишите в чат /shop или /shopping", reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "Редактировать список для существующих пользователей":
            mrkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(len(person)):
                mrkp.add(types.KeyboardButton(str(person[i])))
            msg = bot.send_message(message.chat.id, "Выберете, для кого изменить список покупок", reply_markup=mrkp)
            bot.register_next_step_handler(msg, cart_editing)

    def split_products(message):
        cart.set_splt_persons(person[cart.get_work_id()])
        cart.set_splt_persons(message.text)
        cart.add_person(message.text, cart.get_splt_list())
        mrkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mrkp.add(types.KeyboardButton("Разделить продукт c кем-то еще"), types.KeyboardButton("Закончить список"))
        msg = bot.send_message(message.chat.id, "Продукт будет разделен на нексолько пользователей", reply_markup=mrkp)
        bot.register_next_step_handler(msg, split_handler)


    def split_handler(message):
        if message.text == "Разделить продукт c кем-то еще":
            mrkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(len(person)):
                if person[i] != person[cart.get_work_id()]:
                    mrkp.add(types.KeyboardButton(str(person[i])))
            msg = bot.send_message(message.chat.id, "Выберите или напишите в чат с кем разделить стоимость продукта",
                                   reply_markup=mrkp)
            bot.register_next_step_handler(msg, split_products)
        elif message.text == "Закончить список":
            cart.split_product(cart.get_splt_list(), cart.get_splt_persons())
            cart.set_split_list("")
            cart.set_splt_persons("0")
            mrkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
            mrkp.add(types.KeyboardButton("Завершить список покупок"))
            msg = bot.send_message(message.chat.id, "Для перехода в меню корзины нажмите на кнопку Завершения списка покупок", reply_markup=mrkp)
            bot.register_next_step_handler(msg, cart_packing)



    def cart_packing(message):
        if message.text == "Завершить список покупок":
            mrkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
            it1 = types.KeyboardButton("Добавить пользователя")
            it2 = types.KeyboardButton("Вывести итоговый чек")
            it3 = types.KeyboardButton("Редактировать список для существующих пользователей")
            mrkp.add(it1, it2, it3)
            msg = bot.send_message(message.chat.id, "Что сделать для текущей корзины?", reply_markup=mrkp)
            bot.register_next_step_handler(msg, cart_processing)

        elif message.text == "Разделить продукт":
            mrkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(len(person)):
                mrkp.add(types.KeyboardButton(str(person[i])))
            msg = bot.send_message(message.chat.id, "Выберите или напишите в чат с кем разделить стоимость продукта", reply_markup=mrkp)
            bot.register_next_step_handler(msg, split_products)

        else:
            shop_list = message.text + "\n"
            cart.add_list_of_products(person[cart.get_work_id()], shop_list)
            cart.set_split_list(shop_list)
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton("Завершить список покупок"), types.KeyboardButton("Разделить продукт"))
            msg = bot.send_message(message.chat.id, "Завершение списка покупок или разделение стоимости продуктас другим пользователем", reply_markup=rmk)
            bot.register_next_step_handler(msg, cart_packing)



    @bot.message_handler(commands= ['shop', 'shopping'])
    def working(message):
        person.clear()
        markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_create_cart = types.KeyboardButton("Создать")
        #item_change_cart = types.KeyboardButton("Редактировать")
        markup_inline.add(item_create_cart)
        msg = bot.send_message(message.chat.id, "Что бы вы хотели сделать c корзиной?\nВ будущем опции будут поплняться.",
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
            msg = bot.send_message(message.chat.id, 'Напишите пользователя', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, cart_creation)



    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, "Приветсвую тебя! Надеюсь я смогу помочь вам в организации покупок.\nДля начала работы пропишите в чате /shop или /shopping")


    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

