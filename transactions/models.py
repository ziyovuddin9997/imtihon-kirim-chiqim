from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = "income", "Kirim (Income)"
        EXPENSE = "expense", "Chiqim (Expense)"

    title = models.CharField(
        max_length=200,
        help_text="Transaction title"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Transaction amount"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        help_text="Type of transaction: income or expense"
    )
    category = models.CharField(
        max_length=100,
        help_text="Transaction category (e.g., Food, Salary, Rent)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the transaction"
    )
    date = models.DateField(
        help_text="Date of transaction"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when transaction was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when transaction was last updated"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["transaction_type"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.get_transaction_type_display()})"

    @property
    def formatted_amount(self):
        symbol = "+" if self.transaction_type == self.TransactionType.INCOME else "-"
        return f"{symbol} {self.amount:,.2f}"
