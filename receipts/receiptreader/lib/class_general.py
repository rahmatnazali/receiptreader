# part of `OCR` class
import re

class Vertex(object):
    """
    single point of (x,y)
    """

    def __init__(self, x=None, y=None):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def get_coordinate(self):
        return (self.x, self.y)


class Element(object):
    """
    a string, and its bound
    4 points bound, ordered as: top left, top right, bottom right, bottom left
    """

    def __init__(self, phrase, top_left, top_right, bottom_right, bottom_left):
        self._phrase = phrase
        self._top_left = top_left
        self._top_right = top_right
        self._bottom_right = bottom_right
        self._bottom_left = bottom_left

    @property
    def phrase(self):
        return self._phrase

    @phrase.setter
    def phrase(self, value):
        self._phrase = value

    @property
    def top_left(self):
        return self._top_left

    @top_left.setter
    def top_left(self, value):
        self._top_left = value

    @property
    def top_right(self):
        return self._top_right

    @top_right.setter
    def top_right(self, value):
        self._top_right = value

    @property
    def bottom_right(self):
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, value):
        self._bottom_right = value

    @property
    def bottom_left(self):
        return self._bottom_left

    @bottom_left.setter
    def bottom_left(self, value):
        self._bottom_left = value

    def get_vertices(self):
        return (
            self._top_left,
            self._top_right,
            self._bottom_right,
            self._bottom_left
        )


class OCR(object):

    def __init__(self, fullstring, list_of_element):
        self._fullstring = fullstring
        self._elements = list_of_element

    @property
    def fullstring(self):
        return self._fullstring

    @fullstring.setter
    def fullstring(self, value):
        self._fullstring = value

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        if not isinstance(value, list): raise ValueError("Must be a list of Element")
        self._elements = value

# Part of `Receipt` Class

class BillFrom(object):
    def __init__(self, name = None, address = None):
        self._name = name
        self._address = address

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    def get_dict(self):
        return {
            'name': self.name,
            'address': self.address
        }


class BillTo(object):
    def __init__(self, number = None, pst = None, name = None, address = None, city = None,
                 prov = None, postal = None):
        self._number = number
        self._pst = pst
        self._name = name
        self._address = address
        self._city = city
        self._prov = prov
        self._postal = postal

    def merge_address_string(self, string):
        result = re.findall(r'(.+)\n(.+)\n(.+)\n(.+)(?:\n(.+))*', string)
        if result:
            address, city, prov, postal, leftover = result[0]
            if leftover:
                postal = leftover

            self.address = address
            self.city = city
            self.prov = prov
            self.postal = postal
            # print(address, city, prov, postal, leftover)
        # print(result)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def pst(self):
        return self._pst

    @pst.setter
    def pst(self, value):
        self._pst = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def prov(self):
        return self._prov

    @prov.setter
    def prov(self, value):
        self._prov = value

    @property
    def postal(self):
        return self._postal

    @postal.setter
    def postal(self, value):
        self._postal = value

    def get_dict(self):
        return {
            'custom_number': self.number,
            'custom_PST': self.pst,
            'custom_name': self.name,
            'custom_address': self.address,
            'custom_city': self.city,
            'custom_prov': self.prov,
            'custom_postal': self.postal,
        }


class Bill(object):
    def __init__(self, trans_num = None, card_last_four = None, card_type = None, date = None, time = None,
                 grand_total = None, total_deposit = None, total_gst = None, total_pst = None):
        self._trans_num = trans_num
        self._card_last_four = card_last_four
        self._card_type = card_type
        self._date = date
        self._time = time
        self._grand_total = grand_total
        self._total_deposit = total_deposit
        self._total_gst = total_gst
        self._total_pst = total_pst

    def merge_trans_num_card_date_time(self, trans_num, card_last_four, date, time):
        if self.trans_num is None:
            self.trans_num = trans_num
        if self.card_last_four is None:
            self.card_last_four = card_last_four
        if self.date is None:
            self.date = date
        if self.time is None:
            self.time = time

    def merge_deposit_gst_total(self, total_deposit, total_gst, grand_total):
        if self.total_deposit is None:
            self.total_deposit = total_deposit
        if self.total_gst is None:
            self.total_gst = total_gst
        if self.grand_total is None:
            self.grand_total = grand_total

    @property
    def trans_num(self):
        return self._trans_num

    @trans_num.setter
    def trans_num(self, value):
        self._trans_num = value

    @property
    def card_last_four(self):
        return self._card_last_four

    @card_last_four.setter
    def card_last_four(self, value):
        self._card_last_four = value

    @property
    def card_type(self):
        return self._card_type

    @card_type.setter
    def card_type(self, value):
        self._card_type = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def grand_total(self):
        return self._grand_total

    @grand_total.setter
    def grand_total(self, value):
        self._grand_total = value

    @property
    def total_deposit(self):
        return self._total_deposit

    @total_deposit.setter
    def total_deposit(self, value):
        self._total_deposit = value

    @property
    def total_gst(self):
        return self._total_gst

    @total_gst.setter
    def total_gst(self, value):
        self._total_gst = value

    @property
    def total_pst(self):
        return self._total_pst

    @total_pst.setter
    def total_pst(self, value):
        self._total_pst = value

    def get_dict(self):
        return {
            'trans_num': self.trans_num,
            'card_last_four': self.card_last_four,
            'card_type': self.card_type,
            'date': self.date,
            'time': self.time,
            'grand_total': self.grand_total,
            'total_deposit': self.total_deposit,
            'total_gst': self.total_gst,
            'total_pst': self.total_pst,
        }


class LineItem(object):
    def __init__(self, sku = None, description = None, quantity = None, unit_price = None,
                 line_total = None, tax_code = None, container_deposit = None):
        self._sku = sku
        self._description = description
        self._quantity = quantity
        self._unit_price = unit_price
        self._line_total = line_total
        self._tax_code = tax_code
        self._container_deposit = container_deposit

    def merge_s_d(self, raw_sku, raw_description):
        if self.sku is None:
            self.sku = raw_sku.strip()
        if self.description is None:
            self.description = raw_description.strip()

    def merge_s_d_q_up(self, raw_sku, raw_description, quantity, unit_price):
        if self.sku is None:
            self.sku = raw_sku.strip()
        if self.description is None:
            self.description = raw_description.strip()
        if self.quantity is None:
            self.quantity = quantity
        if self.unit_price is None:
            self.unit_price = unit_price

    def merge_s_d_lt_tc(self, raw_sku, raw_description, line_total, tax_code):
        if self.sku is None:
            self.sku = raw_sku.strip()
        if self.description is None:
            self.description = raw_description.strip()
        if self.line_total is None:
            self.line_total = line_total
        if self.tax_code is None:
            self.tax_code = tax_code

    def merge_s_d_cd(self, raw_sku, raw_description, container_deposit):
        if self.sku is None:
            self.sku = raw_sku.strip()
        if self.description is None:
            self.description = raw_description.strip()
        if self.container_deposit is None:
            self.container_deposit = container_deposit

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, value):
        self._sku = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def unit_price(self):
        return self._unit_price

    @unit_price.setter
    def unit_price(self, value):
        self._unit_price = value

    @property
    def line_total(self):
        return self._line_total

    @line_total.setter
    def line_total(self, value):
        self._line_total = value

    @property
    def tax_code(self):
        return self._tax_code

    @tax_code.setter
    def tax_code(self, value):
        self._tax_code = value

    @property
    def container_deposit(self):
        return self._container_deposit

    @container_deposit.setter
    def container_deposit(self, value):
        self._container_deposit = value

    def get_dict(self):
        return {
            'sku': self.sku,
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'line_total': self.line_total,
            'tax_code': self.tax_code,
            'container_deposit': self.container_deposit,
        }

    def insert_subtotal_and_tax_type(self, regex_result):
        self.line_total = regex_result[0]
        self.tax_code = regex_result[1]


class Receipt(object):

    def __init__(self, bill_from = None, bill_to = None, bill = None, line_items = None):
        self._bill_from = bill_from
        self._bill_to = bill_to
        self._bill = bill
        self._line_items = line_items

    @property
    def bill_from(self):
        return self._bill_from

    @bill_from.setter
    def bill_from(self, value):
        self._bill_from = value

    @property
    def bill_to(self):
        return self._bill_to

    @bill_to.setter
    def bill_to(self, value):
        self._bill_to = value

    @property
    def bill(self):
        return self._bill

    @bill.setter
    def bill(self, value):
        self._bill = value

    @property
    def line_items(self):
        return self._line_items

    @line_items.setter
    def line_items(self, value):
        self._line_items = value

    def get_dict(self):
        return {
            'bill_from': self.bill_from.get_dict() ,
            'bill_to': self.bill_to.get_dict(),
            'bill': self.bill.get_dict(),
            'line_items': [item.get_dict() for item in self.line_items],
        }
