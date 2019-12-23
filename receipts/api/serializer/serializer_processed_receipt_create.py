from rest_framework import serializers
import receiptreader.models

class BillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = receiptreader.models.Bill
        exclude = ('receipt', )

class BillToSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = receiptreader.models.BillTo
        exclude = ('receipt', )

class BillFromSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = receiptreader.models.BillFrom
        exclude = ('receipt', )

class LineItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = receiptreader.models.LineItem
        exclude = ('receipt', )


class ProcessedReceiptSerializer(serializers.ModelSerializer):
    bill = BillSerializer(many=False)
    billto = BillToSerializer(many=False)
    billfrom = BillFromSerializer(many=False)
    line_items = LineItemSerializer(many=True)

    class Meta:
        model = receiptreader.models.ProcessedReceipt
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

        processed_receipt = receiptreader.models.ProcessedReceipt.objects.create(
            **validated_data
        )

        bill_serializer.save(receipt=processed_receipt)
        bill_to_serializer.save(receipt=processed_receipt)
        bill_from_serializer.save(receipt=processed_receipt)
        line_items = line_items_serializer.save(receipt=processed_receipt)

        for i in line_items:
            processed_receipt.line_items.add(i)

        return processed_receipt