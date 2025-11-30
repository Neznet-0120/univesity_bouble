from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User
from core.models import Faculty
from groups_app.models import StudentGroup

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ("student", "Студент"),
        ("teacher", "Преподаватель"),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Кто вы?")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phone", "password1", "password2", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.get('role') == 'student' or (self.instance.role == 'student'):
            self.fields['group'] = forms.ModelChoiceField(
                queryset=StudentGroup.objects.all(),
                label="Ваша группа",
                help_text="Выберите свою учебную группу"
            )
        if self.data.get('role') == 'teacher' or (self.instance.role == 'teacher'):
            self.fields['faculty'] = forms.ModelChoiceField(
                queryset=Faculty.objects.all(),
                label="Факультет",
                help_text="Выберите факультет, где преподаёте"
            )

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        if role == "student" and not cleaned_data.get("group"):
            self.add_error("group", "Студент должен выбрать группу")
        if role == "teacher" and not cleaned_data.get("faculty"):
            self.add_error("faculty", "Преподаватель должен выбрать факультет")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]
        user.status = "pending"
        user.is_active = False

        if user.role == "student":
            user.group = self.cleaned_data.get("group")  # сохраняем группу
            user.faculty = user.group.faculty            # автоматически факультет
        elif user.role == "teacher":
            user.faculty = self.cleaned_data.get("faculty")

        if commit:
            user.save()
            if user.role == "student":
                user.group.students.add(user)  # добавляем студента в группу
        return user    
    