from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum


from .models import (
    Currency,
    FinanceAccount,
    Category,
    Transaction
)

from .serializer import (
    CurrencySerializer,
    FinanceAccountSerializer,
    CategorySerializer,
    TransactionSerializer
)

from .filters import TransactionFilter


class CurrencyViewSet(viewsets.ModelViewSet):

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]


class FinanceAccountViewSet(viewsets.ModelViewSet):

    serializer_class = FinanceAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinanceAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
    @action(detail=False, methods=["get"])
    def stats(self, request):

        qs = self.get_queryset()

        income = qs.filter(
            transaction_type="income"
        ).aggregate(total=Sum("amount"))["total"] or 0

        expense = qs.filter(
            transaction_type="expense"
        ).aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "income": income,
            "expense": expense,
            "balance": income - expense
        })