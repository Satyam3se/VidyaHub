from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    grade = forms.CharField(max_length=50, required=True, label="Current Grade / Class")
    target_exam = forms.ChoiceField(
        choices=Profile.TARGET_EXAM_CHOICES, 
        required=False, 
        label="Target Exam (Optional)",
        widget=forms.Select(attrs={'class': 'glass-select'})
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'target_exam')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            profile = user.profile
            profile.role = 'student'
            profile.grade = self.cleaned_data.get('grade')
            profile.target_exam = self.cleaned_data.get('target_exam') or 'none'
            profile.save()
        return user

class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True, label="Specialized Subject / Expertise")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            profile = user.profile
            profile.role = 'teacher'
            profile.subject = self.cleaned_data.get('subject')
            profile.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'glass-input',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'glass-input',
        'placeholder': 'Password'
    }))

from .models import TeacherNoteUpload, Chapter

class TeacherNoteUploadForm(forms.ModelForm):
    class Meta:
        model = TeacherNoteUpload
        fields = ['chapter', 'pdf_file']
        widgets = {
            'chapter': forms.Select(attrs={'class': 'glass-select'}),
            'pdf_file': forms.FileInput(attrs={'class': 'glass-file-input', 'accept': '.pdf'}),
        }
