from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', RedirectView.as_view(url='users/', permanent=True)),
    path("user/token", TokenObtainPairView.as_view(), name="get_token"),
    path("user/token/refresh", TokenRefreshView.as_view(), name="refresh_token"),
]
