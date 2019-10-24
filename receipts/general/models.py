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

    hierarchy = jsonfield.JSONField(null=True, blank=True, help_text="The most recommended view for user is 'Tree' view")

    def __str__(self):
        if self.name:
            return self.name
        return str(self.id)


class Store(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100)
    location_link = models.URLField(null=True, blank=True, help_text='You can insert google map link here')

    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province_state = models.CharField(max_length=100, verbose_name='Province/State', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        return str(self.id)




# Create your models here.
