"""
URL configuration for university project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from accounts.views import home, faculty_detail
from api.views import LessonViewSet

router = DefaultRouter()
router.register(r'api/lessons', LessonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('accounts/', include("accounts.urls")),
    path('', home, name="home"),
    path("faculty/<slug:slug>/", faculty_detail, name="faculty_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
