from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import Staff, Subscription, Contact, Classes

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializers import UserSerializer, SubscriptionSerializer, ClassesSerializer, StaffSerializer, ContactSerializer

User = get_user_model()

class UserCreateView(CreateAPIView):
    """Endpoint to register a new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # Anyone can register

class UserListView(ListAPIView):
    """Returns a list of users (admins see all, non admin users see only their data)."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all() # Admins can see all users
        return User.objects.filter(id=user.id) # users can see only their data

class UserDetailView(RetrieveAPIView):
    """Returns details of all users (admins see all, non admin users see only their data)."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all() # Admins can access all users
        return User.objects.filter(id=user.id) # users can access only their data




class CreateSubscription(CreateAPIView):
    """Endpoint for creating a new subscription"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return PermissionDenied("Permission required to create a Subscription")
        return Subscription.objects.all()

class ListSubscriptions(ListAPIView):
    """Returns a list of all subscriptions"""
    model = Subscription
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

class DetailsSubscription(RetrieveAPIView):
    """Returns details of all subscriptions"""
    model = Subscription
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]



class CreateStaff(CreateAPIView):
    """Endpoint for  creating a new staff member"""
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return PermissionDenied("Permission required to create a stafff member")
        return Staff.objects.all()
    
class ListStaff(ListAPIView):
    """Returns a list of all staff members"""
    model = Staff
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]

class DetailsStaff(RetrieveAPIView):
    """"Returns the details of all staff accessed from all users"""
    model = Staff
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]



class CreateClasses(CreateAPIView):
    """Endpoint for  creating a new class"""
    serializer_class = ClassesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return PermissionDenied("Permission required to create a class")
        return Classes.objects.all()

class ListClasses(ListAPIView):
    """Returns a list of all classes"""
    model = Classes
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    permission_classes = [AllowAny]

class DetailsClasses(RetrieveAPIView):
    """Returns the details of the classes"""
    model = Classes
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    permission_classes = [AllowAny]




class CreateContactView(CreateAPIView):
    """Allows all users to submit a contact form"""
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact = serializer.save() 

        subject = f"New Contact Form Submission: {contact.subject}"
        message = f""
        Name: {contact.name}
        Email: {contact.email}
        Subject: {contact.subject}

        Message: {contact.message}
        recipient_email = settings.CONTACT_EMAIL # Email where form submissions are sent
        send_mail(subject, message, contact.email, [recipient_email])

        return Response({"message": "Contact form submitted successfully!"}, status=status.HTTP_201_CREATED)

class ListContactView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]





class RegisterView(FormView):
    def register(request):
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect(reverse("index"))
        else:
            form = UserCreationForm()
        return render(request, "registration/register.html", {"form": form})

class LoginView(FormView):
    def login(request):
        if request.method == "POST":
            form = AuthenticationForm(request.POST)
            if form.is_valid():
                return redirect(reverse("index"))
        else:
            form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

class LogoutView(FormView):
    def logout(request):
        if request.method == "POST":
            form = AuthenticationForm(request.POST)
            if form.is_valid():
                return redirect(reverse("index"))
        else:
            form = AuthenticationForm()
        return render(request, "registration/logout.html", {"form": form})