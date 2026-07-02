from rest_framework import serializers

from .models import (
    Currency,
    FinanceAccount,
    Category,
    Transaction
)



class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency

        fields = [
            "id",
            "name",
            "code"
        ]



class FinanceAccountSerializer(serializers.ModelSerializer):

    currency = serializers.SlugRelatedField(
        slug_field="code",
        queryset=Currency.objects.all()
    )


    class Meta:
        model = FinanceAccount

        fields = [
            "id",
            "name",
            "account_type",
            "currency",
            "balance"
        ]



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "category_type"
        ]



class TransactionSerializer(serializers.ModelSerializer):

    account = serializers.SlugRelatedField(
        slug_field='name',
        queryset=FinanceAccount.objects.all()
    )

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    currency = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Currency.objects.all()
    )

    class Meta:
        model = Transaction
        fields = '__all__'