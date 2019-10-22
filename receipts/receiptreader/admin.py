from django.contrib import admin
from receiptreader import models
import receiptreader.helper
import receiptreader.lib.function_parse as function_parse
import receipts.settings

# process all the sub images here
def process_all_images(raw_receipt):
    for anImage in raw_receipt.image_set.all():
        if not anImage.raw_ocr_result:
            result_json_string = receiptreader.helper.textify_binary(anImage)

            if receipts.settings.DEV_MODE:
                raw_full_text = result_json_string
            else:
                json_dict = function_parse.parse_json_string_to_dict(result_json_string)
                raw_full_text = json_dict['fullTextAnnotation']['text']

            anImage.raw_ocr_result = raw_full_text
            anImage.save()

    # parse image.raw_ocr to new receipt
    if raw_receipt.processed_receipt is None and len(raw_receipt.image_set.all()):

        processed_receipt = models.ProcessedReceipt()
        processed_receipt.raw_receipt = raw_receipt
        raw_receipt.pr = processed_receipt

        if len(raw_receipt.image_set.all()) == 1:
            # assuming that it only had one scanned image (not multi images)
            # parse from primitive to django models

            # use this for production/testing
            # anImage = raw_receipt.image_set.all()[0]
            # primitive_receipt_class = receiptreader.helper.parse_raw_text_to_receipt(anImage.raw_ocr_result)

            # now, we use this instead
            dummy_text = "BC LIQUORSTORES\nCELEBRATE LIFE..ENJ\n* * YRESPONSIBLY\nk************\n#123 Kingsgate Mall BCLS\n#122 370 E Broadway\nVancouver , BC V5T 4G5\nPhone:(604) 660-6675\nFax: (604) 872-6895\n************\n********\nCustomer #: 305810\nCust PST #: P10093339\nFOX\nName:\nAddress:\n2321 MAIN STREET\nVANCOUVER\n\u0412\u0421\nBC\nV5T 3C9\n***\n************\n928374\nJAMESON IRISH 1X1.14L\n145.47 G\n3 48.49\nContainer Deposit\n1453\nTANQUERAY LONDON DRY 1X1.14L\n0.60\n101.97 G\n3 @ 33.99\n35.99\nRegularly\nContainer Deposit\n471\nSEAGRAM'S V O 1X1.14L\n0.60\n67.98 G\n2 @ 33.99\nContainer Deposit\n773143\nCAZADORES - BLANCO 1X750ml\n0.40\n127.96 G\n4 31.99\nContainer Deposit\n1438\nCAPTAIN MORGAN WHITE 1X1.14L\n0.40\n66.98 G\n2 @ 33.49\nContainer Deposit\n19557\nLAMARCA PROSECCO 1X187ml\n0.40\n44.34 G\n6 @ 7.39\n7.99\nRegularly\nContainer Deposit\n0.60\nSubtotal\n554.70\nContainer Deposit Subtotal\nG GST 5%\n3.00\n27.74\nTotal\n585.44\nBC Liquor Store # 123\nAug 03 2019 02:46 pmTrans# 301586985795\nTRANSACTION RECORD\nCard:************4112\nA0000000031010\nVISA CREDIT\nTrans Type\nCard Entry\nAuth #\nSequence #\nMerchant ID\nTerminal #\nDate\nTime\nCard Type: VI\nPURCHASE\nC\n:080567\n:001001087\n22109801\nB42210980101\n:08-03-2019\n14:46:0\n:$585.44\nAmount\nTHANK YOU\n00 APPROVED\nRetain this copy for your\nrecords\n*** CUSTOMER COPY ***\n20\nTotal Count of Items\nGST Reg #124542945\nYou saved:\n$9.60\nX 101230 1 5 86 9 85795\n"
            primitive_receipt_class = receiptreader.helper.parse_raw_text_to_receipt(dummy_text)

            processed_receipt.merge_from_primitive(primitive_receipt_class)
            processed_receipt.save()
        else:
            # if multi image is present (e.g. receipt is too large and separated into multiple scanned files)

            # use this for production/testing
            # all_images = [x.raw_ocr_result for x in raw_receipt.image_set.all() if x.raw_ocr_result]
            # merged_fulltext = '\n'.join(all_images)
            # primitive_receipt_class = receiptreader.helper.parse_raw_text_to_receipt(merged_fulltext)

            # now, we use this instead
            dummy_text = "BC LIQUORSTORES\nCELEBRATE LIFE..ENJ\n* * YRESPONSIBLY\nk************\n#123 Kingsgate Mall BCLS\n#122 370 E Broadway\nVancouver , BC V5T 4G5\nPhone:(604) 660-6675\nFax: (604) 872-6895\n************\n********\nCustomer #: 305810\nCust PST #: P10093339\nFOX\nName:\nAddress:\n2321 MAIN STREET\nVANCOUVER\n\u0412\u0421\nBC\nV5T 3C9\n***\n************\n928374\nJAMESON IRISH 1X1.14L\n145.47 G\n3 48.49\nContainer Deposit\n1453\nTANQUERAY LONDON DRY 1X1.14L\n0.60\n101.97 G\n3 @ 33.99\n35.99\nRegularly\nContainer Deposit\n471\nSEAGRAM'S V O 1X1.14L\n0.60\n67.98 G\n2 @ 33.99\nContainer Deposit\n773143\nCAZADORES - BLANCO 1X750ml\n0.40\n127.96 G\n4 31.99\nContainer Deposit\n1438\nCAPTAIN MORGAN WHITE 1X1.14L\n0.40\n66.98 G\n2 @ 33.49\nContainer Deposit\n19557\nLAMARCA PROSECCO 1X187ml\n0.40\n44.34 G\n6 @ 7.39\n7.99\nRegularly\nContainer Deposit\n0.60\nSubtotal\n554.70\nContainer Deposit Subtotal\nG GST 5%\n3.00\n27.74\nTotal\n585.44\nBC Liquor Store # 123\nAug 03 2019 02:46 pmTrans# 301586985795\nTRANSACTION RECORD\nCard:************4112\nA0000000031010\nVISA CREDIT\nTrans Type\nCard Entry\nAuth #\nSequence #\nMerchant ID\nTerminal #\nDate\nTime\nCard Type: VI\nPURCHASE\nC\n:080567\n:001001087\n22109801\nB42210980101\n:08-03-2019\n14:46:0\n:$585.44\nAmount\nTHANK YOU\n00 APPROVED\nRetain this copy for your\nrecords\n*** CUSTOMER COPY ***\n20\nTotal Count of Items\nGST Reg #124542945\nYou saved:\n$9.60\nX 101230 1 5 86 9 85795\n"
            dummy_merged_text = '\n'.join([dummy_text, dummy_text, dummy_text])
            primitive_receipt_class = receiptreader.helper.parse_raw_text_to_receipt(dummy_merged_text)

            processed_receipt.merge_from_primitive(primitive_receipt_class)
            processed_receipt.save()



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
    exclude = ('processed_receipt', 'timestamp')

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
