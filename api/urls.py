from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_auth import CustomAuthToken, LogoutView

router = DefaultRouter()
router.register(r'faculties', views.FacultyViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'classrooms', views.ClassroomViewSet)
router.register(r'groups', views.StudentGroupViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'profiles', views.UserViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomAuthToken.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
