from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('list_subscriptions/', views.ListSubscriptions.as_view(), name='list_subscriptions'),
    path('subscriptions/<str:subscription_name>/', views.DetailsSubscription.as_view(), name='detail_subscriptions'),
    path('<pk>/<str:lastName>/', views.DetailUser.as_view(), name='detail_user'),
    path('list_users/', views.ListUsers.as_view(), name='list_users'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path("acounts/", include("django.contrib.auth.urls")),
]