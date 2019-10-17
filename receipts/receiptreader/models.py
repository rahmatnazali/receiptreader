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
class Output(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    vendor = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    gst = models.DecimalField(max_digits=6, decimal_places=2)
    plt = models.DecimalField(max_digits=6, decimal_places=2)
    deposit = models.DecimalField(max_digits=6, decimal_places=2)
    refnumber = models.CharField(max_length=100)
    customernumber = models.IntegerField()
    customerPST = models.CharField(max_length=100)
    customername = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
