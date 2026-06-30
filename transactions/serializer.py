from rest_framework import serializers
from decimal import Decimal
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(
        choices=Transaction.TransactionType.choices,
        help_text="Tranzaksiya turi: 'kirim' yoki 'chiqim'"
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'title',
            'amount',
            'transaction_type',
            'category',
            'description',
            'date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= Decimal('0.00'):
            raise serializers.ValidationError(
                "Summa 0 dan katta bo'lishi kerak."
            )

        if value > Decimal('999999999999.99'):
            raise serializers.ValidationError(
                "Summa juda katta."
            )

        return value

    def validate_transaction_type(self, value):
        valid_choices = [
            choice[0] for choice in Transaction.TransactionType.choices
        ]

        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Noto'g'ri tranzaksiya turi. Quyidagilardan biri bo'lishi kerak: {', '.join(valid_choices)}"
            )

        return value

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Sarlavha bo'sh bo'lishi mumkin emas."
            )

        return value.strip()

    def validate_category(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Kategoriya bo'sh bo'lishi mumkin emas."
            )

        return value.strip()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['amount'] = float(instance.amount)
        return data