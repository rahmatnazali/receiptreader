from rest_framework import serializers
import receiptreader.models

# receipt model
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = receiptreader.models.Image
        fields = '__all__'

class RawReceiptSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True)
    class Meta:
        model = receiptreader.models.RawReceipt
        fields = '__all__'

    def create(self, validated_data):
        # return super().create(validated_data)
        image_set_list_data = validated_data.pop('image_set')

        raw_receipt = receiptreader.models.RawReceipt.objects.create(**validated_data)
        for image_data in image_set_list_data:
            receiptreader.models.Image.objects.create(
                raw_receipt=raw_receipt,
                **image_data
            )
        return raw_receipt

    def update(self, instance, validated_data):
        image_set_list_data = validated_data.pop('image_set')

        receiptreader.models.RawReceipt.objects.update_or_create(pk=instance.pk, defaults={**validated_data})

        for image_data in image_set_list_data:
            receiptreader.models.Image.objects.update_or_create(pk=image_data.pk, defaults={**image_data})

        return instance