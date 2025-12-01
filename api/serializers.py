from rest_framework import serializers
from core.models import Faculty, Department, Classroom
from groups_app.models import StudentGroup
from schedule.models import Lesson
from news.models import News
from django.contrib.auth import get_user_model

User = get_user_model()


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), source='faculty', write_only=True
    )
    
    class Meta:
        model = Department
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class StudentGroupSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department', write_only=True
    )

    class Meta:
        model = StudentGroup
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    group = serializers.StringRelatedField()
    Classroom = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    group = StudentGroupSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'role_display', 'group']
        read_only_fields = ['id', 'username', 'role', 'group']
        