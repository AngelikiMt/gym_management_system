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
    ("paypal", "PayPal"),
)

class User(AbstractUser):
    dob = models.DateField("Date of Birth")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    modified = models.DateTimeField("Date of Modified", auto_now=True)
    last_signed_in = models.DateTimeField("Last Signed In", auto_now=True)
    subscription = models.ForeignKey("Subscription", on_delete=models.RESTRICT, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    classes_booked = models.ForeignKey("Classes", on_delete=models.RESTRICT, null=True, blank=True)

    payment_method = models.CharField("Payment Method", max_length=20, choices=PAYMENT_METHODS, null=True, blank=True)
    is_paid = models.BooleanField("Subscription Payment", default=False)
    date_of_payment = models.DateTimeField("Date of Payment", auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
'''class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with all permissions."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class StaffUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model for staff users."""
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # Required for admin access

    objects = StaffUserManager()

    USERNAME_FIELD = "email"  # Use email instead of username
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Fields required for createsuperuser

    def __str__(self):
        return self.email
'''
class Subscription(models.Model):
    billing_duration = models.CharField("Billing Duration", max_length=20, choices=BILLING_DURATION_CHOICES, null=True, blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-billing_duration']
        verbose_name_plural = 'Subscription'

    def __str__(self):
        return f"{self.billing_duration}"

#    def save(self, *args, **kwargs):
#        """On save update timestamps"""
#        if not self.id:
#            self.created_at = timezone.now()
#        self.updated_at = timezone.now()
#        return super(Subscription, self).save(*args,**kwargs)

class Classes(models.Model):
    class_name = models.CharField("Class Name", max_length=20)
    class_date = models.DateField("Class Date")
    class_time = models.TimeField("Class Time")
    trainer_name = models.ForeignKey("Staff", on_delete=models.RESTRICT, max_length=50)
    description = models.CharField(help_text="Please, enter class description", max_length=500)
    space = models.CharField(help_text="Please, enter where the class will be located", max_length=50)

    class Meta:
        ordering = ['-class_date', '-class_time']

    def __str__(self):
        return f"{self.class_name} {self.space}"

class Staff(models.Model):
    trainer_name = models.CharField("Name of the trainer", max_length=50)
    trainer_classes = models.ForeignKey("Classes", on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        ordering = ['-trainer_name']
        verbose_name_plural = 'Staff'

    def __str__(self):
        return f"{self.trainer_name}"

class Contact(models.Model):
    pass


