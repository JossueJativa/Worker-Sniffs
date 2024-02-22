"""
URL configuration for WorkSniffs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Vistas normales
    path('', include("startapp.urls")),
    path('manager/', include("manager.urls")),
    path('callcenter/', include("callcenter.urls")),
    path('tecnic/', include("tecnic.urls")),
    path('user/', include("user.urls")),

    # API y documentación
    path('api/', include("API.urls")),
    path('docs/', include_docs_urls(title='WorkSniffs API', public=True)),
]

# Añadimos las rutas de los archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)