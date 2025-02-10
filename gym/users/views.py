import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from .models import User, Subscription, Contact
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .my_utils import send_email
from .forms import ContactForm

def index(request):
    return render(request, 'index.html')


class ListUsers(ListView):
    """Listing all users except of those who are staff memmbers"""

    model = User
    template_name = 'users/list_users.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        qs = User.objects.all().exclude(is_staff=True)
        return qs

    def usersList(request, qs):
        return render(request, 'users/list_users', qs=qs)

class DetailUser(DetailView):
    """User's details"""

    models = User
    template_name = 'users/details_user.html'
    context_object_name = 'user_details'

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
    template_name = "users/contact.html"
    model = Contact
    context_object_name = 'contact'
    form_class = ContactForm

    def form_valid(self, form):
        recipients = form.cleaned_data.get('recipients')
        message = form.cleaned_data.get('message')
        subject = form.cleaned_data.get('subject')
        send_email(subject, recipients, message)

        return super().firm_valid(form)