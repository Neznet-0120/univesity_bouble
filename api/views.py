from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from core.models import Faculty, Department, Classroom
from groups_app.models import StudentGroup
from schedule.models import Lesson
from news.models import News
from .serializers import (
    FacultySerializer, DepartmentSerializer, ClassroomSerializer,
    StudentGroupSerializer, LessonSerializer, NewsSerializer, UserSerializer
)
User = get_user_model()


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permissions_classes = [permissions.IsAuthenticated]


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('day', 'time_start')
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'student' and user.group:
            return Lesson.objects.filter(group=user.group).order_by('day', 'time_start')
        return Lesson.objects.all().order_by('day', 'time_start')
    

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
