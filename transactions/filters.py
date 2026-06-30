import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):

    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TransactionType.choices,
        field_name='transaction_type',
        help_text="Tranzaksiya turini filterlash: kirim yoki chiqim"
    )

    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='icontains',
        help_text="Kategoriya bo'yicha filterlash (katta-kichik harf farqsiz)"
    )

    date = django_filters.DateFilter(
        field_name='date',
        help_text="Aniq sana bo'yicha filterlash (YYYY-MM-DD)"
    )

    date_from = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        help_text="Shu sanadan boshlab tranzaksiyalarni filterlash"
    )

    date_to = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        help_text="Shu sanagacha bo'lgan tranzaksiyalarni filterlash"
    )

    amount_min = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte',
        help_text="Minimal summa bo'yicha filterlash"
    )

    amount_max = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte',
        help_text="Maksimal summa bo'yicha filterlash"
    )

    class Meta:
        model = Transaction
        fields = [
            'transaction_type',
            'category',
            'date',
        ]