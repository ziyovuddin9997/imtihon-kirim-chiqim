import django_filters
from datetime import date, timedelta
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):

    transaction_type = django_filters.CharFilter(field_name="transaction_type")

    currency = django_filters.CharFilter(
        field_name="currency__code",
        lookup_expr="iexact"
    )

    category = django_filters.CharFilter(
        field_name="category__name",
        lookup_expr="icontains"
    )

    date = django_filters.DateFilter(field_name="date")

    date_from = django_filters.DateFilter(
        field_name="date",
        lookup_expr="gte"
    )

    date_to = django_filters.DateFilter(
        field_name="date",
        lookup_expr="lte"
    )

    period = django_filters.CharFilter(method="filter_period")

    class Meta:
        model = Transaction
        fields = [
            "transaction_type",
            "currency",
            "category",
            "date",
            "date_from",
            "date_to",
            "period",
        ]

    def filter_period(self, queryset, name, value):
        today = date.today()

        if value == "daily":
            return queryset.filter(date=today)

        elif value == "weekly":
            return queryset.filter(date__gte=today - timedelta(days=7))

        elif value == "monthly":
            return queryset.filter(
                date__year=today.year,
                date__month=today.month
            )

        return queryset