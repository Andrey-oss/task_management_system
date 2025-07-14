from django import forms
from tms.models import Task

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'text', 'status', 'category', 'deadline', 'image', 'password']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 6}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
