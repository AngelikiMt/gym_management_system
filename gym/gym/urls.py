from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', RedirectView.as_view(url='users/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
