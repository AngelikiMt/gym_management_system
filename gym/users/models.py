from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, BaseUserManager

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
    profile_image = models.ImageField("Profile Image", upload_to='user_images')

    dob = models.DateField("Date of Birth", help_text="Please, enter your date of birth")
    date_of_registration = models.DateTimeField("Date of Registration", editable=False)
    modified = models.DateTimeField("Date of Modified")
    last_signed_in = models.DateTimeField("Last Signed In")
    subscription = models.ForeignKey(Subscription, on_delete=models.RESTRICT, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    classes_booked = models.ForeignKey(Classes, on_delete=models.RESTRICT)

    payment_method = models.CharField("Payment Method", help_text="Please enter user's payment method")
    date_of_payment = models.CharField("Date of Payment")

    is_active = models.BooleanField("Active", default=False)
    is_staff = models.BooleanField("Staff", default=False)
    is_paid = models.BooleanField("Subscription payment", default=False)

    def save(self, *args, **kwargs):
        """On save update timestamps"""
        if not self.id:
            self.date_of_registration = timezone.now()
        self.last_signed_in = timezone.now()
        self.modified = timezone.now()
        self.date_of_payment = timezone.now()
        return super(User, self).save(*args,**kwargs)
    
    class Meta:
        ordering = ['lastName', 'firstName']

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
class StaffUser(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user
    
class Subscription(models.Model):
    subscription_name = models.CharField("Subscription Name", max_length=20)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    billing_duration = models.CharField("Billing Duration", max_length=50, choices=BILLING_DURATION_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['-subscription_name', '-billing_duration']

    def __str__(self):
        return f"{self.subscription_name}"

    def save(self, *args, **kwargs):
        """On save update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(User, self).save(*args,**kwargs)

class Classes(models.Model):
    class_name = models.CharField("Class Name", max_length=20)
    class_date = models.DateField("Class Date")
    class_time = models.TimeField("Class Time")
    trainer = models.ForeignKey(Staff, on_delete=models.RESTRICT)
    description = models.CharField(help_text="Please, enter class description")
    space = models.CharField(help_text="Please, enter where the class will be located")

    class Meta:
        ordering = ['-class_date', '-class_time']

    def __str__(self):
        return f"{self.class_name} {self.space}"

class Staff(models.Model):
    trainer_name = models.CharField("Trainer's name")
    trainer_classes = models.ForeignKey()

    class Meta:
        ordering = ['-trainer_date']

    def __str__(self):
        return f"{self.trainer_name}"


class Contact(models.Model):
    pass

