from django.db import models

BILLING_DURATION_CHOICES = (
    ("MONTHLY", "Monthly"),
    ("QUARTERLY", "Quarterly"),
    ("HALF YEARLY", "Half Yearly"),
    ("YEARLY", "Yearly"),
)

class User(models.Model):
    firstName = models.CharField(max_length=20, help_text="Please, enter your first name")
    lastName = models.CharField(max_length=20, help_text="Please, enter your last name")
    username = models.CharField(unique=True, max_length=20, help_text="Please, enter your username")
    password = models.CharField(max_length=20, help_text="Please, enter your password")
    email = models.EmailField("Email", unique=True, max_length=100)
    dob = models.DateField("Date of Birth", help_text="Please, enter your date of birth")
    date_of_registration = models.DateTimeField("Date of Registration", auto_now=True)
    subscription = models.ForeignKey('Subscription', on_delete=models.RESTRICT, null=True, blank=True)

    is_active = models.BooleanField("Active", default=False)
    is_staff = models.BooleanField("Staff", default=False)
    is_paid = models.BooleanField("Subscription payment", default=False)
    

    class Meta:
        ordering = ['-lastName', '-firstName']

    def __str__(self):
        return self.lastName
    
class Subscription(models.Model):
    subscription_name = models.CharField("Subscription Name", max_length=20)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    billing_duration = models.CharField("Billing Duration", max_length=50, choices=BILLING_DURATION_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['-subscription_name', '-billing_duration']


    def __str__(self):
        return self.subscription_name

