#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient
from doctors.forms import EmergencyAccessForm

def debug_emergency_access():
    """Debug emergency access submission"""
    
    print("🔍 DEBUGGING EMERGENCY ACCESS")
    print("=" * 40)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    # Test form validation
    form_data = {
        'patient_id': patient.patient_id,
        'registration_number': doctor.nmc_registration_number or 'TEST123',
        'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
        'access_reason': 'Emergency test - patient requires immediate medical attention'
    }
    
    form = EmergencyAccessForm(data=form_data)
    
    print(f"\n📋 Form Validation:")
    print(f"Form is valid: {form.is_valid()}")
    
    if not form.is_valid():
        print("Form errors:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return False
    
    print("✅ Form is valid")
    
    # Test doctor validation
    try:
        from patients.utils import doctor_validator
        validation_result = doctor_validator.validate_doctor(
            registration_number=form.cleaned_data['registration_number'],
            state_medical_council=form.cleaned_data['state_medical_council']
        )
        print(f"Doctor validation result: {validation_result}")
    except Exception as e:
        print(f"Doctor validation error: {e}")
        return False
    
    # Test web submission
    print(f"\n🌐 Testing Web Submission:")
    
    client = Client()
    
    # Login
    response = client.post('/doctor/login/', {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    if response.status_code != 302:
        print(f"❌ Login failed: {response.status_code}")
        return False
    
    # Submit emergency access with follow=True to see where it redirects
    response = client.post('/doctor/emergency-access/', form_data, follow=True)
    
    print(f"Response status: {response.status_code}")
    print(f"Response content type: {response['content-type']}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for success indicators
        success_indicators = [
            "Emergency Access Granted",
            patient.first_name,
            patient.patient_id,
            "Emergency Contact",
            "Medical Records"
        ]
        
        print(f"\n📊 Checking Success Indicators:")
        for indicator in success_indicators:
            if indicator in content:
                print(f"✅ {indicator}: Found")
            else:
                print(f"❌ {indicator}: Missing")
        
        # Check for error messages
        if "Invalid patient ID" in content:
            print("❌ Invalid patient ID error")
        elif "Access denied" in content:
            print("❌ Access denied error")
        elif "Your account is not verified" in content:
            print("❌ Account not verified error")
        else:
            print("✅ No error messages found")
    else:
        print(f"❌ Unexpected response status: {response.status_code}")
        return False
    
    return True

if __name__ == '__main__':
    success = debug_emergency_access()
    
    if success:
        print(f"\n🎉 EMERGENCY ACCESS DEBUG COMPLETE!")
    else:
        print(f"\n❌ EMERGENCY ACCESS DEBUG FOUND ISSUES!")
