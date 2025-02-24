from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("list_users/", views.UserListView.as_view(), name="list_users"),
    path("details/<pk>/", views.UserDetailView.as_view(), name="details_user"),
    path("deactivate_user/<pk>/", views.DeactivateUserView.as_view(), name="deactivate_user"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    path("create_subscription/", views.CreateSubscriptionView.as_view(), name="create_subscription"),
    path("list_subscriptions/", views.ListSubscriptionsView.as_view(), name="list_subscriptions"),
    path("subscriptions/<int:pk>/", views.DetailsSubscriptionView.as_view(), name="detail_subscriptions"),
    path("subscriptions/delete/<int:pk>/", views.DeleteSubscriptionView.as_view(), name="delete_subscription"),

    path("create_staff/", views.CreateStaffView.as_view(), name="create_staff"),
    path("list_staff/", views.ListStaffView.as_view(), name="list_staff"),
    path("details_staff/<int:pk>/", views.DetailsStaffView.as_view(), name="details_staff"),
    path("deactivate_staff/<int:pk>/", views.DeactivateStaffView.as_view(), name="deactivate_staff"),
    
    path("create_class/", views.CreateClassesView.as_view(), name="create_class"),
    path("list_classes/", views.ListClassesView.as_view(), name="list_classes"),
    path("details_class/<int:pk>/", views.DetailsClassesView.as_view(), name="details_class"),
    path("delete_class/<int:pk>/", views.DeleteClassesView.as_view(), name="delete_class"),

    path('contact/', views.CreateContactView.as_view(), name='contact_form'),
    path('contacts_list/', views.ListContactView.as_view(), name='contact-list'),
]