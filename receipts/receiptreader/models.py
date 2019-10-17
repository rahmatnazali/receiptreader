from django.db import models
from django.db.models.signals import post_save
from receiptreader.google_vision_api import GoogleVisionApi
import os


# from bs4 import BeautifulSoup

# Create your models here.

# Document storage
class Document(models.Model):
    image = models.ImageField(upload_to='documents')

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return "{}".format(self.image.file)


class RawJson(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    text = models.TextField()
    timeStamp = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.document.image.name


def document_save(sender, instance, **kwargs):
    # print("Instance = ", instance)
    # googlevision = GoogleVisionApi()
    # rawjson = googlevision.ocr_image(instance)
    # RawJson.objects.create(document=instance, text=rawjson)
    pass


# def rawjson_save(sender, instance, **kwargs):

post_save.connect(document_save, sender=Document)


# #Output after document is read by Google vision and JSON is returned


class Receipt(models.Model):
    pass


class BillFrom(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    address = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    """
    bill_from:
    address: '#122 370 E Broadway'
    name: '#123 Kingsgate Mall BCLS'
    """

class Bill(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    transaction_number = models.CharField(max_length=30)
    date = models.DateTimeField()
    time = models.TimeField()
    datetime = models.DateTimeField()

    card_last_four = models.CharField(max_length=4)
    card_type = models.CharField(max_length=2, choices=(
        ('VI', 'VI'),
        ('MC', 'MC'),
        ('DP', 'DP'),
    ))

    grand_total = models.FloatField()
    total_deposit = models.FloatField()
    total_gst = models.FloatField()
    total_pst = models.FloatField()

    """
    bill:
    card_last_four: '4112'
    card_type: VI
    date: 08-03-2019
    grand_total: '585.44'
    time: '14:46:0'
    total_deposit: '3.00'
    total_gst: '27.74'
    total_pst: null
    trans_num: '301586985795'
    """


class BillTo(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    custom_pst = models.CharField(max_length=50)
    custom_address = models.CharField(max_length=50)
    custom_city = models.CharField(max_length=50)
    custom_name = models.CharField(max_length=50)
    custom_number = models.CharField(max_length=50)
    custom_postal = models.CharField(max_length=50)
    custom_prov = models.CharField(max_length=5)

    """
    bill_to:
    custom_PST: P10093339
    custom_address: 2321 MAIN STREET
    custom_city: VANCOUVER
    custom_name: FOX
    custom_number: '305810'
    custom_postal: V5T 3C9
    custom_prov: "BC"
    """

class LineItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)

    container_deposit = models.FloatField()
    description = models.CharField(max_length=100)
    line_total = models.FloatField()
    quantity = models.IntegerField()
    sku = models.IntegerField()
    tax_code = models.CharField(max_length=2, choices=(
        (
            ('G', 'G'),
            ('L', 'L')
        )
    ))
    unit_price = models.FloatField()

    """
    line_items:
    - container_deposit: '0.60'
    description: JAMESON IRISH 1X1.14L
    line_total: '145.47'
    quantity: '3'
    sku: '928374'
    tax_code: G
    unit_price: '48.49'
    """

# class Output(models.Model):
#     document = models.ForeignKey(Document, on_delete=models.CASCADE)
#
#     vendor = models.CharField(max_length=100)
#     date = models.DateField(auto_now=False, auto_now_add=False)
#     total = models.DecimalField(max_digits=6, decimal_places=2)
#     gst = models.DecimalField(max_digits=6, decimal_places=2)
#     plt = models.DecimalField(max_digits=6, decimal_places=2)
#     deposit = models.DecimalField(max_digits=6, decimal_places=2)
#     refnumber = models.CharField(max_length=100)
#     customernumber = models.IntegerField()
#     customerPST = models.CharField(max_length=100)
#     customername = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name

# # Stored item information
# class BCLiquorItem(models.Model):
#   sku = models.IntegerField()
#   name = models.CharField(max_length=100)
#   ml = models.DecimalField(max_digits=15, decimal_places=2)
#   upc = models.IntegerField()

#   def __str__(self):
#         return self.name

# class BCLiquorItemPrice(models.Model):
#   item = models.ForeignKey(BCLiquorItem, on_delete=models.CASCADE)
#   timeStamp = models.DateField(auto_now=False, auto_now_add=True)
#   currentPrice = models.DecimalField(max_digits=6, decimal_places=2)
#   regularPrice = models.DecimalField(max_digits=6, decimal_places=2)

#   def __str__(self):
#         return self.name

# # Line items from OCR matched with existing stored information
# class Line(models.Model):
#   output = models.ForeignKey(Output, on_delete=models.CASCADE)
#   bcliquoritem = models.ForeignKey(BCLiquorItem, on_delete=models.CASCADE)
#   quantity = models.IntegerField()
#   unitPrice = models.DecimalField(max_digits=6, decimal_places=2)
#   # Not sure whether tax is needed or just need total in output
#   # tax = models.CharField(max_length=3)

#   def __str__(self):
#         return self.name
