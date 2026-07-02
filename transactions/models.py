from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Currency(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.code


class FinanceAccount(models.Model):

    PAYMENT_TYPES = (
        ("cash", "Naqd pul"),
        ("card", "Karta"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, unique=True)

    account_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPES
    )

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name


class Category(models.Model):

    CATEGORY_TYPES = (
        ("income", "Kirim"),
        ("expense", "Chiqim"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    name = models.CharField(max_length=100)

    category_type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ("income", "Kirim"),
        ("expense", "Chiqim"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    account = models.ForeignKey(
        FinanceAccount,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(max_digits=15, decimal_places=2)

    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"