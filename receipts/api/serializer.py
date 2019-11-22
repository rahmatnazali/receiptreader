from rest_framework import serializers
from receiptreader.models import ProcessedReceipt, RawReceipt, Image, Bill, BillTo, BillFrom, LineItem
from django.contrib.auth.models import User

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
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bill
        # fields = '__all__'
        exclude = ('receipt', )

class BillToSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = BillTo
        # fields = '__all__'
        exclude = ('receipt', )

class BillFromSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = BillFrom
        # fields = '__all__'
        exclude = ('receipt', )

class LineItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = LineItem
        # fields = '__all__'
        exclude = ('receipt', )


class ProcessedReceiptSerializer(serializers.ModelSerializer):
    bill = BillSerializer(many=False)
    billto = BillToSerializer(many=False)
    billfrom = BillFromSerializer(many=False)
    line_items = LineItemSerializer(many=True)

    class Meta:
        model = ProcessedReceipt
        fields = '__all__'

    def create(self, validated_data):
        bill_serializer = BillSerializer(data=validated_data.pop('bill'))
        bill_serializer.is_valid(raise_exception=True)

        bill_to_serializer = BillToSerializer(data=validated_data.pop('billto'))
        bill_to_serializer.is_valid(raise_exception=True)

        bill_from_serializer = BillFromSerializer(data=validated_data.pop('billfrom'))
        bill_from_serializer.is_valid(raise_exception=True)

        line_items_serializer = LineItemSerializer(data=validated_data.pop('line_items'), many=True)
        line_items_serializer.is_valid(raise_exception=True)

        processed_receipt = ProcessedReceipt.objects.create(
            **validated_data
        )

        bill_serializer.save(receipt=processed_receipt)
        bill_to_serializer.save(receipt=processed_receipt)
        bill_from_serializer.save(receipt=processed_receipt)
        line_items = line_items_serializer.save(receipt=processed_receipt)

        for i in line_items:
            processed_receipt.line_items.add(i)

        return processed_receipt

class VerifyReceipt(serializers.ModelSerializer):
    id = serializers.IntegerField()
    is_verified = serializers.BooleanField()

    class Meta:
        model = ProcessedReceipt
        fields = ('id', 'is_verified')

    def update(self, instance, validated_data):
        print('update!')
        print('instance:', instance)
        print('validated_data:', validated_data)
        instance.is_verified = validated_data['is_verified']
        instance.save()
        return instance

        # bill_data = validated_data.get('bill', None)
        # validated_data.pop('bill')
        # bill = Bill.objects.create(
        #     **bill_data
        # )
        #
        # bill_to_data = validated_data.get('billto', None)
        # validated_data.pop('billto')
        # bill_to = BillTo.objects.create(
        #     **bill_to_data
        # )
        #
        # bill_from_data = validated_data.get('billfrom', None)
        # validated_data.pop('billfrom')
        # bill_from = BillFrom.objects.create(
        #     **bill_from_data
        # )
        #
        # line_items_data = validated_data.get('lineitem_set', [])
        # validated_data.pop('lineitem_set')
        # line_items = [LineItem.objects.create(**single_item) for single_item in line_items_data]
        # print(line_items)
        #
        # processed_receipt = ProcessedReceipt.objects.create(
        #     bill=bill,
        #     billto=bill_to,
        #     billfrom=bill_from,
        #     **validated_data
        # )
        #
        # bill.receipt = processed_receipt
        # bill_to.receipt = processed_receipt
        # bill_from.receipt = processed_receipt
        # bill.save()
        # bill_to.save()
        # bill_from.save()
        #
        # return processed_receipt