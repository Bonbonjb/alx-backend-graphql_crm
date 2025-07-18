from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField()

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
