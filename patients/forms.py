from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, MedicalRecord

class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'profile_image', 'date_of_birth', 'gender', 'blood_group', 'address',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'chronic_diseases', 'allergies'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'chronic_diseases': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['record_type', 'title', 'description', 'file', 'hospital_name', 'doctor_name', 'date_of_record']
        widgets = {
            'date_of_record': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
