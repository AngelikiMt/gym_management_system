from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.core.mail import send_mail
from .forms import ContactForm
from .models import Staff, Subscription

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer

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

class UserDetailView(ListAPIView):
    """Returns a details of all users (admins see all, non admin users see only their data)."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all() # Admins can access all users
        return User.objects.filter(id=user.id) # users can access only their data



class ListSubscriptions(ListView):
    """Listing all subscriptions"""

    model = Subscription
    template_name = 'users/list_subscritions.html'
    context_object_name = 'subscriptions_list'

    def get_queryset(self):
        qs = Subscription.objects.all()
        return qs

class DetailsSubscription(DetailView):
    """Details of subscriptions"""

    model = Subscription
    template_name = 'users/details_subscription.html'
    context_object_name = 'details_subscription'

@login_required
@permission_required('users.can_mark_returned', raise_exception=True)
def get_users_details(request, pk):
    userDetails = get_object_or_404(User, pk=pk)
    return render(request, 'users/detail_user.html', userDetails=userDetails)

class ContactView(FormView):
    template_name = "contact.html"
    model = Contact
    context_object_name = 'contact'
    form_class = ContactForm

    def form_valid(self, form):
        from_email = form.cleaned_data.get('from_email')
        message = form.cleaned_data.get('message')
        subject = form.cleaned_data.get('subject')
        send_mail(subject, from_email, message)

        return super().form_valid(form)
    
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