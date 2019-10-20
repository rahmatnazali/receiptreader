from django.contrib import admin
from receiptreader import models

# Register your models here.


# Custom Admin

# For raw receipt
class ImageInline(admin.TabularInline):
    model = models.Image
    fields = ('binary',)
    min_num = 1

class RawReceiptAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]

    def response_add(self, request, obj, post_url_continue=None):
        print('response_add')
        print(obj)
        print(obj.image_set.all())

        # todo: process all the sub images here

        return super().response_add(request, obj, post_url_continue)


admin.site.register(models.RawReceipt, RawReceiptAdmin)
admin.site.register(models.Image)
# admin.site.register(models.RawJson)


# For processed receipt

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

admin.site.register(models.ProcessedReceipt, ReceiptAdmin)

## Debug purpose
# admin.site.register(models.Bill)
# admin.site.register(models.BillTo)
# admin.site.register(models.BillFrom)
# admin.site.register(models.LineItem)
