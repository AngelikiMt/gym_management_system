from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import Staff, Subscription, Contact, Classes
from .serializers import UserSerializer, SubscriptionSerializer, ClassesSerializer, StaffSerializer, ContactSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserCreateView(CreateAPIView):
    """Endpoint to register a new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserListView(ListAPIView):
    """Admins see all users. Non admin users see only their data."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

class UserDetailView(RetrieveAPIView):
    """Admins see details of all users. Non admin users see only their own details."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all() # Admins can access all users
        return User.objects.filter(id=user.id) # users can access only their data

class DeactivateUserView(UpdateAPIView):
    """Admins can deactivate any user, non admin users can deactivate only their account."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"message": "User deactivated successfully!"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    """Login endpoint that returns JWT token."""
    permission_classes = [AllowAny]

    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """Logout endpoint to blacklist the refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "str(e)"}, status=status.HTTP_400_BAD_REQUEST)


class CreateSubscriptionView(CreateAPIView):
    """Endpoint for creating a new subscription (Admins only)."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAdminUser]

class ListSubscriptionsView(ListAPIView):
    """Returns a list of all subscriptions."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

class DetailsSubscriptionView(RetrieveAPIView):
    """Returns details of a single subscription."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

class DeleteSubscriptionView(DestroyAPIView):
    """Deletes a subscription (Admins only)."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAdminUser]



class CreateStaffView(CreateAPIView):
    """Endpoint for creating a new staff member."""
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdminUser]
    
class ListStaffView(ListAPIView):
    """Returns a list of all staff members"""
    queryset = Staff.objects.filter(is_active="True")
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]

class DetailsStaffView(RetrieveAPIView):
    """"Returns the details of all staff accessed from all users"""
    queryset = Staff.objects.filter(is_active="True")
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]

class DeactivateStaffView(UpdateAPIView):
    """Only admins can deactivate a staff member instead of deleting them."""
    queryset = Staff.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"message": "Staff member deactivated successfully!"}, status=status.HTTP_200_OK)




class CreateClassesView(CreateAPIView):
    """Endpoint for creating a new class (Admins only)."""
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    permission_classes = [IsAdminUser]

class ListClassesView(ListAPIView):
    """Returns a list of all classes."""
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    permission_classes = [AllowAny]

class DetailsClassesView(RetrieveAPIView):
    """Returns the details of a class."""
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    permission_classes = [AllowAny]

class DeleteClassesView(DestroyAPIView):
    """Deletes a class (Admins only)."""
    quesyset = Classes.objects.all()
    serializer_class = ClassesSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("Permission required to delete a class.")
        instance.delete()
        return Response({"message": "Class deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)




class CreateContactView(CreateAPIView):
    """Allows all users to submit a contact form"""
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact = serializer.save() 

        subject = f"New Contact Form Submission: {contact.subject}"
        message = f"""
        Name: {contact.name}
        Email: {contact.email}
        Subject: {contact.subject}
        Message: {contact.message}
        """
        recipient_email = settings.CONTACT_EMAIL
        send_mail(subject, message, contact.email, [recipient_email])

        return Response({"message": "Contact form submitted successfully!"}, status=status.HTTP_201_CREATED)

class ListContactView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]
