from django.contrib import admin
from receiptreader import models

# Register your models here.
admin.site.register(models.Document)

admin.site.register(models.RawJson)
