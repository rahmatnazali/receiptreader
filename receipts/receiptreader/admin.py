from django.contrib import admin
from receiptreader import models
import receiptreader.helper

def process_all_images(obj):
    # todo: process all the sub images here
    for image in obj.image_set.all():
        if not image.raw_ocr_result:
            raw_json = receiptreader.helper.textify_binary(image.absolute_path())
            image.raw_ocr_result = raw_json
            image.save()


# For raw receipt
class ImageInline(admin.TabularInline):
    model = models.Image
    fields = ('binary',)
    min_num = 1

    def get_fields(self, request, obj=None):
        if obj is None:
            return 'binary',
        else:
            return 'binary', 'raw_ocr_result'

class RawReceiptAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]

    def response_add(self, request, obj, post_url_continue=None):
        process_all_images(obj)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        process_all_images(obj)
        return super().response_change(request, obj)

admin.site.register(models.RawReceipt, RawReceiptAdmin)


## Debug purpose
# admin.site.register(models.Image)


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
