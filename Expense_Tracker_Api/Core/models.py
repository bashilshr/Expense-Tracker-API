from django.db import models
from django.contrib.auth.models import User

class ExpenseIncome(models.Model):
    TRANSACTION_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    TAX_TYPE_CHOICES = [
        ('flat', 'Flat'),
        ('percentage', 'Percentage'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_CHOICES)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_type = models.CharField(max_length=10, choices=TAX_TYPE_CHOICES, default='flat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total=models.DecimalField(default=0,max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.transaction_type}) - {self.amount}"
