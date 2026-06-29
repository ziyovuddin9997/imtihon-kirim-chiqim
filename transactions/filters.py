import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):

    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TransactionType.choices,
        field_name='transaction_type',
        help_text="Filter by transaction type: income or expense"
    )

    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='icontains',
        help_text="Filter by category (case-insensitive)"
    )

    date = django_filters.DateFilter(
        field_name='date',
        help_text="Filter by specific date (YYYY-MM-DD)"
    )

    date_from = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        help_text="Filter transactions from this date onwards"
    )

    date_to = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        help_text="Filter transactions up to this date"
    )

    amount_min = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte',
        help_text="Filter transactions with minimum amount"
    )

    amount_max = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte',
        help_text="Filter transactions with maximum amount"
    )

    class Meta:
        model = Transaction
        fields = [
            'transaction_type',
            'category',
            'date',
        ]
