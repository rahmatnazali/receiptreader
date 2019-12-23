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
    id = serializers.IntegerField()

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


    def update(self, instance, validated_data):
        print('update!')
        print('instance', instance, type(instance))
        print('validated_data', validated_data)

        instance_bill = instance.bill
        instance_bill_to = instance.billto
        instance_bill_from = instance.billfrom
        instance_line_items = instance.line_items.all()

        # print(instance_bill)
        # print(instance_bill_to)
        # print(instance_bill_from)
        # print(instance_line_items)
        # return instance


        bill_serializer = BillSerializer(instance_bill, data=validated_data.pop('bill'))
        bill_serializer.is_valid(raise_exception=True)
        bill_serializer.save()

        bill_to_serializer = BillToSerializer(instance_bill_to, data=validated_data.pop('billto'))
        bill_to_serializer.is_valid(raise_exception=True)
        bill_to_serializer.save()

        bill_from_serializer = BillFromSerializer(instance_bill_from, data=validated_data.pop('billfrom'))
        bill_from_serializer.is_valid(raise_exception=True)
        bill_from_serializer.save()

        # update line items
        line_items_validated_data_raw = validated_data.pop('line_items')
        line_items_instance = {item.id: item for item in instance_line_items}
        line_items_validated_data_dict = {item['id']:item for item in line_items_validated_data_raw}


        print(line_items_instance)
        print(line_items_validated_data_raw)
        print(line_items_validated_data_dict)
        # return instance



        for line_item_id, line_item_data, in line_items_validated_data_dict.items():
            a_line_item = line_items_instance.get(line_item_id, None)
            if a_line_item is None:
                line_item_data.pop('id')
                print('create')
                print(line_item_data)
                # receiptreader.models.LineItem.objects.create(receipt=instance, **line_item_data)
            else:
                print('update')
                print(line_item_data)
                # receiptreader.models.LineItem.objects.update(receipt=instance, **line_item_data)

            receiptreader.models.LineItem.objects.update_or_create(**line_item_data)

        # perform deletion
        for line_item_id, line_item_data in line_items_instance.items():
            if line_item_id not in line_items_validated_data_dict:
                line_item_data.delete()


        # line_items_serializer = LineItemSerializer(data=validated_data.pop('line_items'), many=True)
        # line_items_serializer.is_valid(raise_exception=True)

        return instance