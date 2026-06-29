from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'formatted_amount',
        'transaction_type_display',
        'category',
        'date',
        'created_at',
    ]

    list_filter = [
        'transaction_type',
        'category',
        'date',
        'created_at',
    ]

    search_fields = [
        'title',
        'category',
        'description',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'formatted_amount_display',
    ]

    fieldsets = (
        ('Transaction Information', {
            'fields': (
                'title',
                'amount',
                'formatted_amount_display',
                'transaction_type',
            )
        }),
        ('Details', {
            'fields': (
                'category',
                'description',
                'date',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )

    date_hierarchy = 'date'
    ordering = ['-created_at']

    actions = [
        'mark_as_income',
        'mark_as_expense',
    ]


    def transaction_type_display(self, obj):
        if obj.transaction_type == Transaction.TransactionType.INCOME:
            color = 'green'
            label = 'Kirim (Income)'
        else:
            color = 'red'
            label = 'Chiqim (Expense)'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            label
        )
    transaction_type_display.short_description = 'Type'


    def formatted_amount(self, obj):
        symbol = '+' if obj.transaction_type == Transaction.TransactionType.INCOME else '−'
        return f"{symbol} {obj.amount:,.2f}"
    formatted_amount.short_description = 'Amount'


    def formatted_amount_display(self, obj):
        if obj.transaction_type == Transaction.TransactionType.INCOME:
            color = 'green'
            symbol = '+'
        else:
            color = 'red'
            symbol = '−'

        return format_html(
            '<span style="color: {}; font-weight: bold; font-size: 1.2em;">{} {}</span>',
            color,
            symbol,
            f"{obj.amount:,.2f}"
        )
    formatted_amount_display.short_description = 'Formatted Amount'

    def mark_as_income(self, request, queryset):
        updated = queryset.update(transaction_type=Transaction.TransactionType.INCOME)
        self.message_user(request, f'{updated} transaction(s) marked as income.')
    mark_as_income.short_description = 'Mark selected as Income (Kirim)'


    def mark_as_expense(self, request, queryset):
        updated = queryset.update(transaction_type=Transaction.TransactionType.EXPENSE)
        self.message_user(request, f'{updated} transaction(s) marked as expense.')
    mark_as_expense.short_description = 'Mark selected as Expense (Chiqim)'


    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        queryset = self.get_queryset(request)
        income_total = queryset.filter(
            transaction_type=Transaction.TransactionType.INCOME
        ).aggregate(total=Sum('amount'))['total'] or 0

        expense_total = queryset.filter(
            transaction_type=Transaction.TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or 0

        balance = income_total - expense_total

        extra_context['summary_stats'] = {
            'total_income': income_total,
            'total_expense': expense_total,
            'balance': balance,
            'total_transactions': queryset.count(),
        }

        return super().changelist_view(request, extra_context)


    class Media:
        css = {
            'all': ('admin/css/transaction_admin.css',)
        }
