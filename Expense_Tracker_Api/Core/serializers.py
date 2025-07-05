from .models import ExpenseIncome
from rest_framework import serializers
from decimal import Decimal

class ExpenseSerilizer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseIncome
        exclude = ['user']
        read_only_fields = ('created_at', 'updated_at', 'total')

    def validate(self, data):
        tax = data.get('tax')
        if tax is not None and (tax < 0 or tax > 100):
            raise serializers.ValidationError("Tax must be between 0 and 100.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        amount = validated_data.get('amount')
        tax = validated_data.get('tax', Decimal('0'))
        tax_type = validated_data.get('tax_type', 'flat').lower()

        if tax_type == 'flat':
            total = amount + tax
        else:
            total = amount + (amount * tax / 100)

        validated_data['total'] = total
        return super().create(validated_data)

    def update(self, instance, validated_data):
        allowed_fields = ['tax_type', 'transaction_type', 'title', 'description', 'tax']
        for field in validated_data:
            if field not in allowed_fields:
                raise serializers.ValidationError({
                    field: f"Field '{field}' is not allowed to be updated."
                })

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        tax = instance.tax
        amount = instance.amount
        tax_type = instance.tax_type.lower()

        if tax_type == 'flat':
            instance.total = amount + tax
        else:
            instance.total = amount + (amount * tax / 100)

        instance.save()
        return instance
