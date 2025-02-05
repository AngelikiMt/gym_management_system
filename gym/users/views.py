import datetime

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import User, Subscription
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'index.html')


class ListUsers(ListView):
    """Listing all users"""

    model = User
    template_name = 'users/list_users.html'
    context_object_name = 'user_list'
    queryset = User.objects.all().order_by('-lastName')

class DetailUser(DetailView):
    """User's details"""

    models = User
    template_name = 'users/details_user.html'
    context_object_name = 'user_details'
    queryset = User.objects.all()


class ListSubscriptions(ListView):
    """Listing all subscriptions"""

    model = Subscription
    template_name = 'users/list_subscritions.html'
    context_object_name = 'subscriptions_list'
    queryset = Subscription.objects.all()

class DetailsSubscription(DetailView):
    """Details of subscriptions"""

    model = Subscription
    template_name = 'users/details_subscription.html'
    context_object_name = 'details_subscription'

@login_required
@permission_required('users.can_mark_returned', raise_exception=True)
def get_users_details(request, pk):
    userDetails = get_object_or_404(User, pk=pk)
    return render(request, 'users/detail_user.html')