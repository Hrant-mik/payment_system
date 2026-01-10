from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(help_text="Price in cents")

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def total_amount(self):
        return sum(i.item.price * i.quantity for i in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
