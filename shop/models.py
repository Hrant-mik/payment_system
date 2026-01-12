from django.db import models

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(help_text="Price in cents")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')
    @property
    def price_dollars(self):
        return self.price / 100
    
    def __str__(self):
        return f"{self.name} ({self.currency.upper()})"
    
    


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    currency = models.CharField(max_length=3, choices=Item.CURRENCY_CHOICES, default='usd')

    
    @property
    def total_amount(self):
        total_cents = sum(oi.item.price * oi.quantity for oi in self.items.all())
        return total_cents / 100

    @property
    def total_amount_dollars(self):
        return float(self.total_amount)

    def __str__(self):
        return f"Order {self.id} - {self.status}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
