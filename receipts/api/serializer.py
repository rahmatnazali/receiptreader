from rest_framework import serializers
from receiptreader.models import ProcessedReceipt, RawReceipt, Image, Bill, BillTo, BillFrom, LineItem
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

class UserLoginSerializer(serializers.ModelSerializer):
    """
    User serializer for login purpose
    """
    class Meta:
        model = User
        fields = ("username", 'password')

class TokenSerializer(serializers.Serializer):
    """
    JWT Token serializer
    """
    token = serializers.CharField(max_length=255)


# receipt model
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class RawReceiptSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True)
    class Meta:
        model = RawReceipt
        fields = '__all__'

    def create(self, validated_data):
        # return super().create(validated_data)
        image_set_list_data = validated_data.pop('image_set')

        raw_receipt = RawReceipt.objects.create(**validated_data)
        for image_data in image_set_list_data:
            Image.objects.create(
                raw_receipt=raw_receipt,
                **image_data
            )
        return raw_receipt

    def update(self, instance, validated_data):
        image_set_list_data = validated_data.pop('image_set')

        RawReceipt.objects.update_or_create(pk=instance.pk, defaults={**validated_data})

        for image_data in image_set_list_data:
            Image.objects.update_or_create(pk=image_data.pk, defaults={**image_data})

        return instance


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        # fields = '__all__'
        exclude = ('receipt', )

class BillToSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillTo
        # fields = '__all__'
        exclude = ('receipt', )

class BillFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillFrom
        # fields = '__all__'
        exclude = ('receipt', )

class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        # fields = '__all__'
        exclude = ('receipt', )


class ProcessedReceiptSerializer(serializers.ModelSerializer):
    bill = BillSerializer(many=False)
    billto = BillToSerializer(many=False)
    billfrom = BillFromSerializer(many=False)
    lineitem_set = LineItemSerializer(many=True)

    class Meta:
        model = ProcessedReceipt
        fields = '__all__'

    def create(self, validated_data):
        bill_data = validated_data.get('bill', None)
        validated_data.pop('bill')
        bill = Bill.objects.create(
            **bill_data
        )

        bill_to_data = validated_data.get('billto', None)
        validated_data.pop('billto')
        bill_to = BillTo.objects.create(
            **bill_to_data
        )

        bill_from_data = validated_data.get('billfrom', None)
        validated_data.pop('billfrom')
        bill_from = BillFrom.objects.create(
            **bill_from_data
        )

        line_items_data = validated_data.get('lineitem_set', [])
        validated_data.pop('lineitem_set')
        line_items = [LineItem.objects.create(**single_item) for single_item in line_items_data]
        print(line_items)

        processed_receipt = ProcessedReceipt.objects.create(
            bill=bill,
            billto = bill_to,
            billfrom = bill_from,
            **validated_data
        )

        bill.receipt = processed_receipt
        bill_to.receipt = processed_receipt
        bill_from.receipt = processed_receipt
        bill.save()
        bill_to.save()
        bill_from.save()

        return processed_receipt
