import receiptreader.lib.function_regex as function_regex

invalid_description = [
    'transaction',
    'record'
]

def count_alphabet(string):
    count = 0
    for char in string:
        if char.isalpha():
            count += 1
    return count

def count_number(string):
    count = 0
    for char in string:
        if char.isdigit():
            count += 1
    return count



def clean_sku(string_sku):
    return string_sku.strip()

def is_description_valid(string_description):
    description_lower = string_description.lower().strip()
    for e in invalid_description:
        if e in description_lower:
            return False
        if description_lower.strip().isdigit():
            return False

    if count_alphabet(description_lower) < 3:
        return False

    return True

def clean_description(string_description):
    return string_description.strip()

def clean_quantity_and_unit_price(string_q_up):
    string_q_up = string_q_up.strip()

    quantity, unit_price = function_regex.group_quantity_unit_price(string_q_up)
    if quantity is None and unit_price is None: return None, None

    unit_price = function_regex.cleanse_unit_price(unit_price)
    # print(quantity, unit_price)

    return quantity, unit_price
