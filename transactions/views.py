from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from decimal import Decimal

from .models import Transaction
from .serializer import TransactionSerializer
from .filters import TransactionFilter


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['title', 'category', 'description']

    ordering_fields = ['created_at', 'amount', 'date', 'title']
    ordering = ['-created_at'] 

    def get_queryset(self):
        queryset = super().get_queryset()

        transaction_type = self.request.query_params.get('transaction_type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset

    def perform_create(self, serializer):
        
        serializer.save()

    def perform_update(self, serializer):
 
        serializer.save()

    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):

        queryset = self.get_queryset()


        income_total = queryset.filter(
            transaction_type=Transaction.TransactionType.INCOME
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense_total = queryset.filter(
            transaction_type=Transaction.TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        balance = income_total - expense_total

        statistics = {
            'total_income': float(income_total),
            'total_expense': float(expense_total),
            'balance': float(balance),
            'count_income': queryset.filter(
                transaction_type=Transaction.TransactionType.INCOME
            ).count(),
            'count_expense': queryset.filter(
                transaction_type=Transaction.TransactionType.EXPENSE
            ).count(),
        }

        return Response(statistics, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        queryset = self.get_queryset()


        income_total = queryset.filter(
            transaction_type=Transaction.TransactionType.INCOME
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense_total = queryset.filter(
            transaction_type=Transaction.TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')


        category_breakdown = []
        for category in queryset.values_list('category', flat=True).distinct():
            category_income = queryset.filter(
                category=category,
                transaction_type=Transaction.TransactionType.INCOME
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            category_expense = queryset.filter(
                category=category,
                transaction_type=Transaction.TransactionType.EXPENSE
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            category_breakdown.append({
                'category': category,
                'income': float(category_income),
                'expense': float(category_expense),
                'balance': float(category_income - category_expense),
            })

        summary = {
            'overall': {
                'total_income': float(income_total),
                'total_expense': float(expense_total),
                'balance': float(income_total - expense_total),
                'total_transactions': queryset.count(),
            },
            'by_category': category_breakdown,
        }

        return Response(summary, status=status.HTTP_200_OK)
