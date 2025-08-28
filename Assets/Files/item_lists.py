import random


def get_items_test(first, qty):
    item_price_test = {"Wood": 10,
                       "Salt": 5,
                       "Meat": 5,
                       "Grain": 3}
    items_list_test = []

    for item, price in item_price_test.items():
        if not first:
            qty = random.randint(1, 10)
        new_item = (item, price, qty)
        items_list_test.append(new_item)

    first = True
    # print(items_list_test)
    return items_list_test, first, qty


get_items_test(first=False, qty=0)
