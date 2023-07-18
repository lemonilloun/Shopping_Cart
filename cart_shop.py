def writting(cart_list):
    res = ""
    personal_cart = ""
    delim = "------------------------------------"
    delim_2 = "##################################"

    chat_id = cart_list["chat_id"]
    cart_id = cart_list["cart_id"]
    products_per_person = cart_list["persons"]
    split_products_list = cart_list["splits"]
    split_products = {}
    split_persons = []

    k = len(products_per_person)
    cur_per = 0
    total_sum = 0
    sum_per_person = 0
    splt_check = bool(split_products_list)


    for prod in split_products_list:
        lines = prod.split('\n')
        lines = [line for line in lines if line]

        reslt = []

        for line in lines:
            part = line.split('-')[0]
            reslt.append(part)
            split_products[part] = str(len(split_products_list[prod]))

        for pers in split_products_list[prod]:
            if pers not in split_persons:
                split_persons.append(pers)


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
                if prod[0] in split_products and per in split_persons:
                    cost = (int(prod[2]) * int(prod[1]))/int(split_products[prod[0]])
                    personal_cart += prod[0] + " - " + str(cost) + "р.\n"
                    sum_per_person += cost
                else:
                    cost = int(prod[2]) * int(prod[1])
                    personal_cart += prod[0] + " (" + prod[2] + " шт.)" + " - " + str(cost) + "р.\n"
                    sum_per_person += cost

            elif len(prod) == 2:
                if prod[0] in split_products and per in split_persons:
                    cost = int(prod[1])/int(split_products[prod[0]])
                    personal_cart += prod[0] + " - " + str(cost) + "р.\n"
                    sum_per_person += cost
                else:
                    personal_cart += prod[0] + " - " + prod[1] + "р.\n"
                    sum_per_person += int(prod[1])

        personal_cart += "\n" + str(sum_per_person) + "\n" + delim + "\n"
        total_sum += sum_per_person
        sum_per_person = 0
    #Header
    res += "Коризина № " + str(cart_id) + "\n" + delim_2 + "\n"

    #Main
    res += personal_cart + delim_2 + "\n"

    #Total
    res += "Total: " + str(total_sum)  + "р.\n"
    if k > 1:
        if splt_check == False:
            res += "Если скидываться : " + str(total_sum / k) + "р."

        #personal_cart += delim + str(per) + "\n" + cart_list[per] + delim

    #print(res)
    return res


#cart_list = {'chat_id': 923034297, 'cart_id': 52, 'persons': {'лиза': 'хлеб-50\nпиво-100\nкиндер delice-70\n', 'леся': 'хлеб-50\nпиво-100\nкиндер delice-70\n'}, 'splits': {'хлеб-50\nпиво-100\nкиндер delice-70\n': ['лиза', 'леся']}}
#print(writting(cart_list))