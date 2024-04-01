# razorpay/models.py

from django.db import models
from logi.models import User  # Import the custom user model




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use the custom user model
    medicines = models.ManyToManyField('logi.Medicine', through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=50, default='PENDING')  # 'PENDING', 'PAID', 'FAILED', etc.
    order_date=models.DateField(auto_now_add=True)
    delivery_date=models.DateField(null=True)
    prescription = models.ForeignKey('logi.Prescription', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_delivery_person = models.ForeignKey('logi.DeliveryPerson', on_delete=models.SET_NULL, null=True, blank=True)
    is_delivery_person = models.BooleanField(default=False)






    # Add other fields as needed

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    medicine = models.ForeignKey('logi.Medicine', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cart=   models.ForeignKey('logi.cart',on_delete=models.CASCADE)
    # Add other fields as needed

# logi.models.py

from django.db import models
from main_project.models import Order  # Import the Order model

class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Tracking for Order ID {self.order.id}'


from django.db import models
from logi.models import Medicine

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    company_name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # New field for active status

    # Add other fields as needed

    def __str__(self):
        return f'Purchase Order #{self.id} for {self.medicine.medicine_name}'


# models.py

# models.py
from django.db import models
from .models import Order

class Sales(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sales for Order {self.order.id}"

from django.db import models
from logi.models import Medicine

class ManufacturerSales(models.Model):
    manufacturer = models.CharField(max_length=255)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.manufacturer} - {self.medicine.medicine_name} Sales'

    class Meta:
        unique_together = ('manufacturer', 'medicine')


from django.db import models

class MonthlyStats(models.Model):
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['month', 'year']


class Delivery(models.Model):
    order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    delivery_person = models.ForeignKey('logi.DeliveryPerson', on_delete=models.CASCADE)

    def __str__(self):
        return f"Delivery for Order ID: {self.order_id} (Status: {self.status})"
