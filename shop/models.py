from django.db import models
from django.contrib.auth.models import User


class Computer(models.Model):
    """
    Model representing a computer or laptop with configurable components.
    """
    id = models.AutoField(primary_key=True)
    case_type = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    memory = models.IntegerField()
    storage = models.IntegerField()
    graphics_card = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    peripherals = models.TextField(blank=True, null=True)
    is_laptop = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='computers')

    def __str__(self):
        device_type = "Laptop" if self.is_laptop else "Desktop"
        return f"{self.color} {self.case_type} {device_type} ({self.processor}, {self.memory}GB RAM)"


class Order(models.Model):
    """
    Model representing an order for a custom-built computer.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    computer = models.OneToOneField(Computer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')


    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"