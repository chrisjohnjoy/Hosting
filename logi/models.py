# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

   is_customer= models.BooleanField(default=False)
   is_employee= models.BooleanField(default=False)
   is_delivery_person = models.BooleanField(default=False)

   name=models.CharField(max_length=50)

class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)

class Customer(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone_number=models.CharField(max_length=20)
    address=models.CharField(max_length=50,null=True,blank=True)
    cart = models.OneToOneField('Cart', on_delete=models.SET_NULL, null=True, blank=True)

class Employee(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone_number=models.CharField(max_length=20)
    designation = models.CharField(max_length=30)


# from django.db import models
# from django.core.validators import MinValueValidator

# class Medicine(models.Model):
#     medicine_id = models.AutoField(primary_key=True)
#     medicine_name = models.CharField(max_length=255, unique=True)
#     prescription = models.BooleanField(default=False)
#     type_of_sell = models.CharField(max_length=255)
#     manufacturer = models.CharField(max_length=255)
#     salt = models.CharField(max_length=255)
#     mrp = models.DecimalField(max_digits=10, decimal_places=2)
#     wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
#     uses = models.TextField()
#     alternate_medicines = models.TextField()
#     side_effects = models.TextField()
#     how_to_use = models.TextField()
#     chemical_class = models.CharField(max_length=255)
#     habit_forming = models.BooleanField(default=False)
#     therapeutic_class = models.CharField(max_length=255)
#     action_class = models.CharField(max_length=255)
#     how_it_works = models.TextField()

#     in_stock = models.IntegerField()
#     added_on = models.DateField(auto_now_add=True)
#     medicine_image = models.ImageField(upload_to='medicine_images/')
#     requires_prescription = models.BooleanField(default=False)

#     STATUS_CHOICES = [
#         ('active', 'Active'),
#         ('inactive', 'Inactive'),
#         # Add more choices as needed
#     ]

#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

#     def __str__(self):
#         return self.medicine_name

#     def clean(self):
#         # Custom validation logic
#          if self.mfg_date and self.exp_date and self.mfg_date > self.exp_date:
#             raise ValidationError(_('Manufacturing date cannot be after the expiry date.'))

#     class Meta:
#         verbose_name_plural = 'Medicines'

from decimal import Decimal



class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=255)
    requires_prescription = models.BooleanField(default=False)
    type_of_sell = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    uses = models.TextField(null=True,blank=True)
    alternate_medicines = models.TextField(null=True,blank=True)
    side_effects = models.TextField(null=True,blank=True)
    how_to_use = models.TextField(null=True,blank=True)
    chemical_class = models.CharField(max_length=255)
    habit_forming = models.BooleanField(default=False)
    therapeutic_class = models.CharField(max_length=255)
    action_class = models.CharField(max_length=255)
    how_it_works = models.TextField(null=True, blank=True)    
    batch_no = models.CharField(max_length=255)
    exp_date = models.DateField()
    mfg_date = models.DateField()
    in_stock = models.IntegerField()
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_date = models.DateField(auto_now_add=True)
    medicine_image = models.ImageField(upload_to='medicine_images/', null=True, blank=True)
    active_status = models.BooleanField(default=True)


    def __str__(self):
        return self.medicine_name

    def clean(self):
        # Custom validation logic
        if self.mfg_date and self.exp_date and self.mfg_date > self.exp_date:
            raise ValidationError(_('Manufacturing date cannot be after the expiry date.'))

    
    
    class Meta:
        verbose_name_plural = 'Medicines'


class Prescription(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    prescription_file = models.FileField(upload_to='prescriptions/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return f'Prescription for Cart ID {self.cart.id}'



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicines = models.ManyToManyField('Medicine', through='CartItem')
    active = models.BooleanField(default=True)


    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    requires_prescription = models.BooleanField(default=False)

    # Your other fields and methods here

    def save(self, *args, **kwargs):
        # Automatically set prescription_required based on the associated medicine
        self.requires_prescription = self.medicine.requires_prescription
        super(CartItem, self).save(*args, **kwargs)

    def get_total_price(self):
        return self.medicine.mrp * self.quantity

from django.db import models
from django.core.validators import MinValueValidator

class MedicineStockAlert(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    threshold = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Alert when stock falls below this quantity"
    )
    last_triggered = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the alert was last triggered"
    )

    def __str__(self):
        return f"Alert for {self.medicine.medicine_name}"

    class Meta:
        verbose_name_plural = 'Medicine Stock Alerts'


from django.utils import timezone

class PrescriptionVerification(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Verification for Prescription ID {self.prescription.id}'

    def save(self, *args, **kwargs):
        if not self.verified_at:
            self.verified_at = timezone.now()
        super().save(*args, **kwargs)

class demo(models.Model):
    medical_id=models.AutoField(primary_key=True)
    Name=models.CharField(max_length=255)
    num=models.CharField(max_length=255)