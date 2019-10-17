import re

regex_library = {
    'sku': re.compile(r'\n(\d{3,})\n[A-Z]{2}'),
    'subtotal_and_tax_type': re.compile(r'(\d+.\d+) (G)'),
    'description': [
        re.compile(r'[A-Z- \']{5,50}\d[xX]\d+\.\d+L'),          # for pattern like 1x1.14L, like CAPTAIN MORGAN WHITE 1X1.14L'
        re.compile(r'[A-Z0-9- \']{5,50}\d[xX]\d+[Mm][Ll]\n'),   # for pattern that ends with ml, like 'CAZADORES BLANCO 1X750ml\n' 'EL JIMADOR BLANCO 1X750mL\n'
        re.compile(r'[A-Z0-9- \']{5,50}\d[xX]\d+[Mm]\n'),       # for missing the 'l' on 'ml', like "ROAD13 HONEST JOHN'S ROSE 1X750m\n", 'CAPTAIN MORGAN - SPICED 1X750m\n'
    ],
    'container_deposit': re.compile(r'[01]\.\d0'),
    'quantity_unit_price': [
        re.compile(r'\d+ @ \d+\.\d\d'),     # for normal one, like ['2 @ 29.99']
        re.compile(r'\d+ \d+\.\d\d'),       # for missing @, like ['3 48.49', '4 31.99']
        re.compile(r'\n\d{4}[.,]\d\d\n'),   # for no space and dot is acted like comma, like ['1220,49', '\n1216.49\n']
    ],
    'misc': {
        'split_quantity_unit_price': re.compile(r'(\d+) @ (\d+\.\d\d)'),
        'quantity_unit_price_grouper': [
            re.compile(r'(\d+) *@ *(\d+\.\d\d)'),   # for normal one, like ['2 @ 29.99']
            re.compile(r'(\d+) (\d+\.\d\d)'),       # for missing @, like ['3 48.49', '4 31.99']
            re.compile(r'(\d{2})(\d{2}[.,]\d\d)'),  # for no space and dot is acted like comma, like ['1220,49', '\n1216.49\n']

        ]
    }
}


def re_findall(regex, string):
    return regex.findall(string)


def re_parse_line_total_and_tax_type(string):
    return re_findall(regex_library['subtotal_and_tax_type'], string)


def order_by_string_index(needle, haystack):
    return haystack.find(needle)


def re_parse_sku(string):
    result = re_findall(regex_library['sku'], string)
    return result


def re_parse_description(string):
    result = []
    for regex in regex_library['description']:
        result += re_findall(regex, string)
    # print(result)
    sorted_list = sorted(result, key=lambda r: string.find(r))
    cleaned_list = [x.replace('\n', '') for x in sorted_list]
    return cleaned_list


def re_parse_container_deposit(string):
    result = re_findall(regex_library['container_deposit'], string)

    # remove the last element if it was a subtotal
    float_result = [float(x) for x in result]
    if len(float_result) >= 3 and sum(float_result[:-1]) == float_result[-1]:
        del float_result[-1]
    return [str(x) for x in float_result]


def cleanse_unit_price(string):
    if ',' in string:
        return string.replace(',', '.')
    else:
        return string


def group_quantity_unit_price(string):
    for pattern in regex_library['misc']['quantity_unit_price_grouper']:
        result = pattern.findall(string)
        if len(result):
            return result[0]
    return None, None


def re_parse_quantity_unit_price(string):
    result = []
    for pattern in regex_library['quantity_unit_price']:
        result += re_findall(pattern, string)
    # print(result)

    sorted_list = sorted(result, key=lambda r: string.find(r))
    # print(sorted_list)

    grouped_list = [group_quantity_unit_price(x) for x in sorted_list]
    # print(grouped_list)

    cleaned_list = [(unit, cleanse_unit_price(price)) for unit, price in grouped_list]
    # print(cleaned_list)

    return cleaned_list


# for mk2 ===============================================
re_magic = r'.*?'


## Bill From
re_bill_from_name = r'\*\n(#*[A-Za-z0-9\'#& ]+?)\n'
re_bill_from_address = r'(.+?)\n'

## Bill To
re_bill_to_customer = r'Customer #: (\d+)\n'
re_bill_to_customer_pst = r'Cust PST #: (P\d+)\n'
re_bill_to_name = r'([A-Z]+)\nName:'
re_bill_to_address = r'Address:\n(.*?)\n\*'

## Bill
re_bill_card = r'Card: *\*{4,12}(\d\d\d\d)'
re_bill_transaction_number = r'[A-Za-z]{3} \d\d \d\d\d\d \d\d:\d\d .+?(\d+)'
re_bill_date = r'(\d\d-\d\d-\d\d\d\d)'
re_bill_time = r'(\d\d:\d\d:\d{1,2})'

re_subtotal_deposit_gst_total_1 = r'Subtotal{}([\d,]+\.\d\d){}(\d+\.\d0){}([\d,]+\.\d\d){}([\d,]+\.\d\d)'.format(re_magic, re_magic, re_magic, re_magic)
re_subtotal_deposit_gst_total_2 = r'([\d,]+\.\d\d)\nSubtotal{}(\d+\.\d0){}([\d,]+\.\d\d){}([\d,]+\.\d\d)'.format(re_magic, re_magic, re_magic)

re_card_type = r'Card Type{}:{{0,1}}{}(VI|MC|DP)'.format(re_magic, re_magic)


## Line Items
re_sku = r'(\n\d+\n)'
re_description = [
    r'[A-Z- \']{5,50}\d[xX]\d+\.\d+L',
    r'[A-Z0-9- \']{5,50}\d[xX]\d+[Mm][Ll]*\n',
    r'[A-Z0-9- \']{5,50}(?:\d[xX])*\d+[Mm][Ll]*\n',
    r'[A-Z0-9- \']{5,50}(?:\d[xX])*\d+[Mm]*[Ll]*[ \]]*\n',
    r'[A-Z- \']{5,50}\n',
]
re_final_description = '(' + '|'.join(re_description) + ')'

re_line_total_tax_code = r'(\d{2,5}\.\d\d) {0,1}([GL])[.]*\n'
re_final_total_tax_code = r'(?:{})'.format(re_line_total_tax_code)

re_quantity_unit_price = [
    r'\d+ *@ *\d+\.\d\d',   # for normal one, like ['2 @ 29.99']
    r'\d+ \d+\.\d\d',       # for missing @, like ['3 48.49', '4 31.99']
    r'\d{4}[\.,]\d\d\n',    # for no space and dot is acted like comma, like ['1220,49', '\n1216.49\n']
]
re_final_quantity_unit_price = r'({})'.format('|'.join(re_quantity_unit_price))

re_container_deposit = [
    r'\d{,2}\.\d0',
]
re_final_container_deposit = r'({})'.format('|'.join(re_container_deposit))

"""
The key is abbreviation of its attribute
s_d: SKU, Description
s_d_lt_tc: SKU, Description, Line Total, Tax Code
s_d_q_up: SKU, Description, Quantity @ Unit Price
s_d_cd: SKU, Description, Container Deposit
"""
re_dict = {
    ## Bill From
    'bill_from': r'{}{}'.format(re_bill_from_name, re_bill_from_address),

    ## Bill To
    'bill_to_2': r'{}{}{}{}{}{}'.format(re_bill_to_customer, re_magic, re_bill_to_customer_pst, re_bill_to_name, re_magic, re_bill_to_address),

    ## Bill
    'bill_trans_num_card_date_time': r'{}{}{}{}{}{}{}'.format(re_bill_transaction_number, re_magic, re_bill_card, re_magic, re_bill_date, re_magic, re_bill_time),
    're_subtotal_deposit_gst_total_1': re_subtotal_deposit_gst_total_1,
    're_subtotal_deposit_gst_total_2': re_subtotal_deposit_gst_total_2,
    'bill_card_type': re_card_type,

    ## Line Items
    's_d': r'{}{}{}'.format(re_sku, re_magic, re_final_description),
    's_d_q_up': r'{}{}{}{}{}'.format(re_sku, re_magic, re_final_description, re_magic, re_final_quantity_unit_price),
    's_d_lt_tc': r'{}{}{}{}{}'.format(re_sku, re_magic, re_final_description, re_magic, re_final_total_tax_code),
    's_d_cd': r'{}{}{}{}{}'.format(re_sku, re_magic, re_final_description, re_magic, re_final_container_deposit),

    # below are currently unused, but let's just save it here in case of future affairs
    's_d_q_up_cd': r'{}{}{}{}{}{}{}'.format(re_sku, re_magic, re_final_description, re_magic, re_final_quantity_unit_price, re_magic, re_final_container_deposit),
    'lt_tc_s_d': r'{}{}{}{}{}'.format(re_final_total_tax_code, re_magic, re_sku, re_magic, re_final_description),
    's_d_lt_tc_q_up': r'{}{}{}{}{}{}{}'.format(re_sku, re_magic, re_final_description, re_magic, re_final_total_tax_code, re_magic, re_final_quantity_unit_price),
}

## Bill From
def re_find_all_bill_from(string):
    result = re.findall(re_dict['bill_from'], string, re.DOTALL)
    return result

## Bill To
def re_find_all_bill_to(string):
    result = re.findall(re_dict['bill_to_2'], string, re.DOTALL)
    return result

## Bill
def re_find_all_bill_trans_num_card_date_time(string):
    result = re.findall(re_dict['bill_trans_num_card_date_time'], string, re.DOTALL)
    return result

def re_find_all_re_subtotal_deposit_gst_total_1(string):
    result = re.findall(re_dict['re_subtotal_deposit_gst_total_1'], string, re.DOTALL)
    return result

def re_find_all_re_subtotal_deposit_gst_total_2(string):
    result = re.findall(re_dict['re_subtotal_deposit_gst_total_2'], string, re.DOTALL)
    return result

def re_find_all_re_card_type(string):
    result = re.findall(re_dict['bill_card_type'], string, re.DOTALL)
    return result


## Line Items

def re_find_all_s_d(string):
    # result = re_findall_dotall(regex_library_mk2['s_d'], string)
    result = re.findall(re_dict['s_d'], string, re.DOTALL)
    return result


def re_find_all_s_d_q_up(string):
    # result = re_findall_dotall(regex_library_mk2['s_d_q_up'], string)
    result = re.findall(re_dict['s_d_q_up'], string, re.DOTALL)
    return result


def re_find_all_s_d_lt_tc(string):
    # result = re_findall_dotall(regex_library_mk2['s_d_lt_tc'], string)
    result = re.findall(re_dict['s_d_lt_tc'], string, re.DOTALL)
    return result


def re_find_all_s_d_cd(string):
    result = re.findall(re_dict['s_d_cd'], string, re.DOTALL)
    return result
