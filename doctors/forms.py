from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor

class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nmc_registration_number = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    specialization = forms.ChoiceField(
        choices=Doctor.SPECIALIZATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    hospital_name = forms.CharField(
        max_length=200, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    hospital_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
        required=True
    )
    years_of_experience = forms.IntegerField(
        min_value=0, 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    medical_license_number = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    state_medical_council = forms.ChoiceField(
        choices=[
            ('Andhra Pradesh Medical Council', 'Andhra Pradesh Medical Council'),
            ('Tamil Nadu Medical Council', 'Tamil Nadu Medical Council'),
            ('Karnataka Medical Council', 'Karnataka Medical Council'),
            ('Maharashtra Medical Council', 'Maharashtra Medical Council'),
            ('Delhi Medical Council', 'Delhi Medical Council'),
            ('Gujarat Medical Council', 'Gujarat Medical Council'),
            ('Uttar Pradesh Medical Council', 'Uttar Pradesh Medical Council'),
            ('West Bengal Medical Council', 'West Bengal Medical Council'),
            ('Rajasthan Medical Council', 'Rajasthan Medical Council'),
            ('Other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Doctor
        fields = (
            'first_name', 'last_name', 'email', 'phone_number', 'nmc_registration_number',
            'specialization', 'hospital_name', 'hospital_address', 'years_of_experience',
            'medical_license_number', 'state_medical_council', 'password1', 'password2'
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.nmc_registration_number = self.cleaned_data['nmc_registration_number']
        user.specialization = self.cleaned_data['specialization']
        user.hospital_name = self.cleaned_data['hospital_name']
        user.hospital_address = self.cleaned_data['hospital_address']
        user.years_of_experience = self.cleaned_data['years_of_experience']
        user.medical_license_number = self.cleaned_data['medical_license_number']
        user.state_medical_council = self.cleaned_data['state_medical_council']
        if commit:
            user.save()
        return user

class EmergencyAccessForm(forms.Form):
    patient_id = forms.CharField(max_length=20, required=True, help_text="Enter patient's unique ID")
    access_reason = forms.CharField(widget=forms.Textarea, required=True, help_text="Describe the emergency situation")
    registration_number = forms.CharField(max_length=50, required=True, help_text="Enter your NMC registration number")
    state_medical_council = forms.ChoiceField(choices=[
        ('Andhra Pradesh Medical Council', 'Andhra Pradesh Medical Council'),
        ('Tamil Nadu Medical Council', 'Tamil Nadu Medical Council'),
        ('Karnataka Medical Council', 'Karnataka Medical Council'),
        ('Maharashtra Medical Council', 'Maharashtra Medical Council'),
        ('Delhi Medical Council', 'Delhi Medical Council'),
        ('Gujarat Medical Council', 'Gujarat Medical Council'),
        ('Uttar Pradesh Medical Council', 'Uttar Pradesh Medical Council'),
        ('West Bengal Medical Council', 'West Bengal Medical Council'),
        ('Rajasthan Medical Council', 'Rajasthan Medical Council'),
        ('Other', 'Other'),
    ], required=True, help_text="Select your state medical council")
