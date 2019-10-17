from django.contrib import admin
from receiptreader import models

# Register your models here.
admin.site.register(models.Document)

admin.site.register(models.RawJson)


# Custom Admin

class BillInline(admin.StackedInline):
    model = models.Bill

class BillToInline(admin.StackedInline):
    model = models.BillTo

class BillFromInline(admin.StackedInline):
    model = models.BillFrom

class LineItemInline(admin.StackedInline):
    model = models.LineItem

class ReceiptAdmin(admin.ModelAdmin):
    inlines = [
        BillFromInline,
        BillToInline,
        BillInline,
        LineItemInline
    ]

admin.site.register(models.Receipt, ReceiptAdmin)

## Debug purpose
# admin.site.register(models.Bill)
# admin.site.register(models.BillTo)
# admin.site.register(models.BillFrom)
# admin.site.register(models.LineItem)
