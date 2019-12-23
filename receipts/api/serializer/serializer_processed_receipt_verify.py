from rest_framework import serializers
import receiptreader.models

class VerifyReceipt(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField()

    class Meta:
        model = receiptreader.models.ProcessedReceipt
        fields = ('id', 'is_verified')

    def update(self, instance, validated_data):
        print('update!')
        print('instance:', instance)
        print('validated_data:', validated_data)
        instance.is_verified = validated_data['is_verified']
        instance.save()
        return instance