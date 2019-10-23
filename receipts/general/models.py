from django.db import models
import jsonfield

# vendor, store, etc

"""
Vendor can have multiple Store
Store can have multiple Receipt (both RawReceipt and ProcessedReceipt)

vendor:
name, street address, city, province/state, phone, email, yaml schema...everything except for name and yaml can be null
i guess yaml could be null

for now no need for vendor location, it wouldnt be needed very often


"""

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province_state = models.CharField(max_length=100, verbose_name='Province/State', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    hierarchy = jsonfield.JSONField(null=True, blank=True)

# class Store(models.Model):
#     pass



# Create your models here.
