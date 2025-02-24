from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Subscription, Staff, Contact, Classes

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "dob", "modified", "last_signed_in", "subscription", "discount", "classes_booked", "payment_method", "is_paid", "date_of_payment"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        """Creates a new user, ensuring password is properly hashed."""
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user 
        
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "subscription", "fees", "description", "created_at", "updated_at"]

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id", "trainer_last_name", "trainer_first_name", "trainer_classes", "is_active"]

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "phone_number", "email", "subject", "message", "created_at"]

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ["id", "class_name", "class_date", "class_time", "trainer", "description", "location_of_the_class", "capacity"]