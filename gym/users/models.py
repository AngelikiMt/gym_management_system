from django.db import models
from django.contrib.auth.models import AbstractUser

BILLING_DURATION_CHOICES = (
    ("MONTHLY", "Monthly"),
    ("3MONTHS", "3Months"),
    ("HALF YEARLY", "Half Yearly"),
    ("YEARLY", "Yearly"),
)

PAYMENT_METHODS = (
    ("CARD", "Credit/Debit Card"),
    ("CASH", "Cash"),
    ("INSTALLMENTS", "Installments"),
    ("PAYPAL", "PayPal"),
)

CAPACITY = (
    ("5", "5"),
    ("10", "10"),
    ("15", "15"),
    ("20", "20"),
)

class User(AbstractUser):
    dob = models.DateField("Date of Birth", null=True, blank=True)
    user_phone_number = models.CharField(max_length=50, blank=True, null=True)
    modified = models.DateTimeField("Date of Modified", auto_now=True)
    last_signed_in = models.DateTimeField("Last Signed In", auto_now=True)
    subscription = models.ForeignKey("Subscription", on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    classes_booked = models.ForeignKey("Classes", on_delete=models.SET_NULL, null=True, blank=True)

    payment_method = models.CharField("Payment Method", max_length=20, choices=PAYMENT_METHODS, null=True, blank=True)
    is_paid = models.BooleanField("Subscription Payment", default=False)
    date_of_payment = models.DateTimeField("Date of Payment", auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Subscription(models.Model):
    billing_duration = models.CharField(max_length=20, choices=BILLING_DURATION_CHOICES, null=True, blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['billing_duration']
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.billing_duration} - €{self.fees}"

class Classes(models.Model):
    class_name = models.CharField(max_length=20, null=True, blank=True)
    class_date = models.DateField(null=True, blank=True)
    class_time = models.TimeField(null=True, blank=True)
    trainer = models.ForeignKey("Staff", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    location_of_the_class = models.CharField(max_length=50, null=True, blank=True)
    max_capacity = models.IntegerField(choices=CAPACITY, null=True, blank=True)

    class Meta:
        ordering = ['-class_date', '-class_time']

    def __str__(self):
        return f"{self.class_name} {self.location_of_the_class}"

class Staff(models.Model):
    trainer_last_name = models.CharField(max_length=50, null=True, blank=True)
    trainer_first_name = models.CharField(max_length=50, null=True, blank=True)
    trainer_phone_number = models.CharField(max_length=100, null=True, blank=True)
    trainer_email = models.EmailField(max_length=50, blank=True, null=True)
    trainer_classes = models.ManyToManyField("Classes", blank=True)
    hiring_day = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['trainer_last_name', 'trainer_first_name']
        verbose_name_plural = 'Staff'

    def __str__(self):
        return f"{self.trainer_last_name} {self.trainer_first_name}"

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"] 

    def __str__(self):
        return f"message from {self.name} - {self.subject}"
