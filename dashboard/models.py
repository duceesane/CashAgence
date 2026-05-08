from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Wallet(models.Model):
    agent        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    name         = models.CharField(max_length=100)
    logo         = models.CharField(max_length=10, default='WL')
    location     = models.CharField(max_length=200)
    epos_id      = models.CharField(max_length=50, unique=True)
    balance      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    block_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    commission   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    dep_rate     = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    with_rate    = models.DecimalField(max_digits=5, decimal_places=2, default=2.0)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return f"{self.name} — {self.agent.get_full_name() or self.agent.username}"

    @property
    def total_deposits(self):
        return self.transactions.filter(txn_type='deposit').aggregate(
            total=models.Sum('amount'))['total'] or 0

    @property
    def total_payouts(self):
        return self.transactions.filter(txn_type='payout').aggregate(
            total=models.Sum('amount'))['total'] or 0

    @property
    def total_volume(self):
        return self.total_deposits + self.total_payouts


class Transaction(models.Model):
    TXN_TYPES = [('deposit', 'Deposit'), ('payout', 'Payout')]
    STATUS    = [('success', 'Success'), ('pending', 'Pending'), ('failed', 'Failed')]
    agent = models.ForeignKey(User,on_delete=models.CASCADE)
    wallet     = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    phone = models.IntegerField(null=True)
    amount = models.FloatField()
    txn_type   = models.CharField(max_length=10, choices=TXN_TYPES)
    type_money = models.CharField(max_length=40)
    status     = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        sign = '+' if self.txn_type == 'deposit' else '-'
        return f"{sign}${self.amount} —  ({self.created_at:%Y-%m-%d})"

    @property
    def is_deposit(self):
        return self.txn_type == 'deposit'

    @property
    def display_amount(self):
        sign = '+' if self.is_deposit else '-'
        return f"{sign}${self.amount:,.2f}"

