"""shinet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from shinet.settings import env

schema_view = get_schema_view(
    openapi.Info(
        title="Shinet API",
        default_version='v1',
        description="Shinet api documentations",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    url=env.str('SWAGGER_URL')
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.auth.urls')),
    path('api/v1/registration/', include('users.registration.urls')),
    path('api/v1/recovery/', include('users.recovery.urls')),
    path('api/v1/tokens/', include('tokens.urls')),
    path('api/v1/services/', include('services.urls')),
    path('api/v1/locations/', include('users.locations.urls')),
    path('api/v1/subscriptions/', include('subscriptions.urls')),
    path('api/v1/slots/', include('slots.urls')),
    path('api/v1/clients/unregistered/', include('users.unregistered_clients.urls')),
    path('api/v1/clients/', include('users.clients.urls')),
    path('api/v1/verification/', include('verification.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


