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
    def __str__(self):
        return str(self.id)

    pass


class BillFrom(models.Model):
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, null=True, blank=True)

    address = models.CharField(max_length=250, verbose_name='Address', null=True, blank=True)
    name = models.CharField(max_length=250, verbose_name='Name', null=True, blank=True)

    """
    bill_from:
    address: '#122 370 E Broadway'
    name: '#123 Kingsgate Mall BCLS'
    """


class Bill(models.Model):
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, null=True, blank=True)

    transaction_number = models.CharField(max_length=30, verbose_name='Transaction Number', null=True, blank=True)
    date = models.DateTimeField(verbose_name='Date', null=True, blank=True)
    time = models.TimeField(verbose_name='Time', null=True, blank=True)
    datetime = models.DateTimeField(verbose_name='Date Time', null=True, blank=True)

    card_last_four = models.CharField(max_length=4, verbose_name='Card Last 4 Number', null=True, blank=True)
    card_type = models.CharField(max_length=2, choices=(
        ('VI', 'VI'),
        ('MC', 'MC'),
        ('DP', 'DP'),
    ), verbose_name='Card Type', null=True, blank=True)

    grand_total = models.FloatField(verbose_name='Grand Total', null=True, blank=True)
    total_deposit = models.FloatField(verbose_name='Total Deposit', null=True, blank=True)
    total_gst = models.FloatField(verbose_name='Total GST', null=True, blank=True)
    total_pst = models.FloatField(verbose_name='Total PST', null=True, blank=True)

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
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, null=True, blank=True)

    custom_pst = models.CharField(max_length=50, verbose_name='PST', null=True, blank=True)
    custom_number = models.CharField(max_length=50, verbose_name='Number', null=True, blank=True)
    custom_name = models.CharField(max_length=50, verbose_name='Name', null=True, blank=True)
    custom_address = models.CharField(max_length=50, verbose_name='Address', null=True, blank=True)

    custom_city = models.CharField(max_length=50, verbose_name='City', null=True, blank=True)
    custom_prov = models.CharField(max_length=5, verbose_name='Prov', null=True, blank=True)
    custom_postal = models.CharField(max_length=10, verbose_name='Postal', null=True, blank=True)

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
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, null=True, blank=True)

    sku = models.IntegerField(verbose_name='SKU')
    description = models.CharField(verbose_name='Item Name', max_length=100)
    unit_price = models.FloatField(verbose_name='Unit Price', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Quantity', null=True, blank=True)
    line_total = models.FloatField(verbose_name='Unit Sub Total', null=True, blank=True)

    container_deposit = models.FloatField(null=True, blank=True)
    tax_code = models.CharField(max_length=2, choices=(
        (
            ('G', 'G'),
            ('L', 'L')
        )
    ), null=True, blank=True)

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
