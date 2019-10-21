import receiptreader.lib.function_regex as function_regex
import receiptreader.lib.function_cleaner as function_cleaner
from .lib import class_general
from receiptreader.google_vision_api import GoogleVisionApi
import pathlib
import pytz
import datetime

def merge_date_time(raw_date, raw_time):
    cleaned_date = raw_date if raw_date is not None else ''
    cleaned_time = raw_time if raw_time is not None else ''

    merged_date_time = '{} {}'.format(cleaned_date, cleaned_time).strip()

    if ' ' in merged_date_time:
        cleaned_datetime = datetime.datetime.strptime(merged_date_time, '%m-%d-%Y %H:%M:%S')
    elif len(cleaned_date):
        cleaned_datetime = datetime.datetime.strptime(merged_date_time, '%m-%d-%Y')
    elif len(cleaned_time):
        cleaned_datetime = datetime.datetime.strptime(merged_date_time, '%H:%M:%S')
    else:
        return None

    cleaned_datetime = cleaned_datetime.replace(tzinfo=pytz.UTC)
    return cleaned_datetime

def textify_binary(anImage):
    return anImage.absolute_path() # todo: remove this line for production / testing
    try:
        googlevision = GoogleVisionApi()
        result_json_string = googlevision.ocr_image(anImage)
        return result_json_string
    except Exception as e:
        print(e)
    return ""

def merge_s_d(dict_line_item, string):
    result_s_d = function_regex.re_find_all_s_d(string)
    # print('Found possible SKU and Description:', len(result_s_d))
    for raw_sku, raw_description in result_s_d:
        if function_cleaner.is_description_valid(raw_description):
            cleaned_sku = raw_sku.strip()
            aLineItem = class_general.LineItem()
            aLineItem.merge_s_d(raw_sku, raw_description)
            dict_line_item[cleaned_sku] = aLineItem
    return dict_line_item

def merge_s_d_q_up(dict_line_item, string):
    result_s_d_q_up = function_regex.re_find_all_s_d_q_up(string)
    # print('Found possible Quantity and Unit Price:', len(result_s_d_q_up))

    for raw_sku, raw_description, raw_quantity_and_unit_price in result_s_d_q_up:
        if function_cleaner.is_description_valid(raw_description):
            cleaned_sku = raw_sku.strip()
            quantity, unit_price = function_cleaner.clean_quantity_and_unit_price(raw_quantity_and_unit_price)

            if cleaned_sku in dict_line_item:
                dict_line_item[cleaned_sku].merge_s_d_q_up(raw_sku, raw_description, quantity, unit_price)
            else:
                aLineItem = class_general.LineItem()
                aLineItem.merge_s_d_q_up(raw_sku, raw_description, quantity, unit_price)
                dict_line_item[cleaned_sku] = aLineItem
    return dict_line_item

def merge_s_d_lt_tc(dict_line_item, string):
    result_s_d_lt_tc = function_regex.re_find_all_s_d_lt_tc(string)
    # print('Found possible Line Total and Tax Code:', len(result_s_d_lt_tc))

    for raw_sku, raw_description, line_total, tax_code in result_s_d_lt_tc:
        if function_cleaner.is_description_valid(raw_description):
            cleaned_sku = raw_sku.strip()

            if cleaned_sku in dict_line_item:
                dict_line_item[cleaned_sku].merge_s_d_lt_tc(raw_sku, raw_description, line_total, tax_code)
            else:
                aLineItem = class_general.LineItem()
                aLineItem.merge_s_d_lt_tc(raw_sku, raw_description, line_total, tax_code)
                dict_line_item[cleaned_sku] = aLineItem
    return dict_line_item

def merge_s_d_cd(dict_line_item, string):
    result_s_d_cd = function_regex.re_find_all_s_d_cd(string)
    # print('Found possible Container Deposit:', len(result_s_d_cd))

    for raw_sku, raw_description, container_deposit in result_s_d_cd:
        if function_cleaner.is_description_valid(raw_description):
            cleaned_sku = raw_sku.strip()

            if cleaned_sku in dict_line_item:
                dict_line_item[cleaned_sku].merge_s_d_cd(raw_sku, raw_description, container_deposit)
            else:
                aLineItem = class_general.LineItem()
                aLineItem.merge_s_d_cd(raw_sku, raw_description, container_deposit)
                dict_line_item[cleaned_sku] = aLineItem
    return dict_line_item


def compute_bill_from(string):
    bill_from = class_general.BillFrom()
    result = function_regex.re_find_all_bill_from(string)
    if len(result):
        name, address = result[0]
        bill_from.name = name
        bill_from.address = address
    return bill_from

def compute_bill_to(string):
    bill_to = class_general.BillTo()
    result = function_regex.re_find_all_bill_to(string)
    if result:
        result = result[0]
        bill_to_number, bill_to_pst, bill_to_name, bill_to_raw_address = result
        bill_to.number = bill_to_number
        bill_to.pst = bill_to_pst
        bill_to.name = bill_to_name
        bill_to.merge_address_string(bill_to_raw_address)
    return bill_to

def compute_bill(string):
    bill = class_general.Bill()
    result_1 = function_regex.re_find_all_bill_trans_num_card_date_time(string)
    if result_1:
        trans_num, card_last_four, date, time = result_1[0]
        bill.merge_trans_num_card_date_time(trans_num, card_last_four, date, time)

    result_2 = function_regex.re_find_all_re_subtotal_deposit_gst_total_1(string)
    if result_2:
        subtotal, total_deposit, total_gst, grand_total = result_2[0]
        bill.merge_deposit_gst_total(total_deposit, total_gst, grand_total)
    else:
        result_2 = function_regex.re_find_all_re_subtotal_deposit_gst_total_2(string)
        if result_2:
            subtotal, total_deposit, total_gst, grand_total = result_2[0]
            bill.merge_deposit_gst_total(total_deposit, total_gst, grand_total)

    result_card_type = function_regex.re_find_all_re_card_type(string)
    if result_card_type:
        card_type = result_card_type[0]
        bill.card_type = card_type

    return bill

def compute_line_item(string):
    dict_line_item = {}

    # phase 1: get all possible sku and description, and save it to dict
    dict_line_item = merge_s_d(dict_line_item, string)

    # phase 2: fill with possible information according to its SKU
    dict_line_item = merge_s_d_q_up(dict_line_item, string)
    dict_line_item = merge_s_d_lt_tc(dict_line_item, string)
    dict_line_item = merge_s_d_cd(dict_line_item, string)

    return [x[1] for x in dict_line_item.items()]

def parse_single_json_string(string):

    bill_to = compute_bill_to(string)
    bill_from = compute_bill_from(string)
    bill = compute_bill(string)
    line_items = compute_line_item(string)

    # compile to recepit
    aReceipt = class_general.Receipt(
        bill_from=bill_from,
        bill_to=bill_to,
        bill=bill,
        line_items=line_items
    )
    return aReceipt

def parse_raw_text_to_receipt(raw_string):
    # json_dict = function_parse.parse_json_to_dict(json_file_pointer)
    # aReceipt = parse_single_json_string(json_dict['fullTextAnnotation']['text'])
    aReceipt = parse_single_json_string(raw_string)
    return aReceipt
