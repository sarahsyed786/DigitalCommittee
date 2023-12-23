from django import forms
from .models import Enrollment,Interest

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = []

class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['package_name', 'message']