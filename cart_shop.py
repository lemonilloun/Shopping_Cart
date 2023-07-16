def writting(cart_list):
    res = ""
    personal_cart = ""
    delim = "------------------------------------"

    chat_id = cart_list["chat_id"]
    cart_id = cart_list["cart_id"]
    products_per_person = cart_list["persons"]
    #print(products_per_person)

    k = len(products_per_person)
    cur_per = 0
    total_sum = 0
    sum_per_person = 0

    for per in products_per_person:
        lines = products_per_person[per].split('\n')
        lines = [line for line in lines if line]

        result = []

        for line in lines:
            parts = line.split('-')
            result.append(parts)

        personal_cart += "\n" + per + ":\n"
        for prod in result:
            if len(prod) == 3:
                personal_cart += prod[0] + " (" + prod[2] + " шт.)" + " - " + str(int(prod[2]) * int(prod[1])) + "р." + "\n"
                sum_per_person += int(prod[2]) * int(prod[1])
            elif len(prod) == 2:
                personal_cart += prod[0] + " - " + prod[1]
                sum_per_person += int(prod[1])
        personal_cart += "\n" + str(sum_per_person) + "\n" + delim + "\n"
        total_sum += sum_per_person
    print(personal_cart)

        #personal_cart += delim + str(per) + "\n" + cart_list[per] + delim


    #return res


cart_list = {'chat_id': 546077575, 'cart_id': 19, 'persons': {'тома': 'молоко-45-2\nхлеб-76-1\nтрубочка со сгущенкой-103-2\n', 'лесЯ': 'киндеры-516-3\n'}}
print(writting(cart_list))