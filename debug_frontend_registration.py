#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.forms import DoctorRegistrationForm
from doctors.models import Doctor

def debug_frontend_registration():
    """Debug frontend registration process"""
    
    print("🔍 Debugging Frontend Registration...")
    
    # Simulate frontend form data
    form_data = {
        'first_name': 'Frontend',
        'last_name': 'Test',
        'email': 'frontend.test@example.com',
        'phone_number': '9876543299',
        'nmc_registration_number': 'FRONTEND123',
        'specialization': 'GENERAL',
        'hospital_name': 'Frontend Test Hospital',
        'hospital_address': '789 Frontend Street',
        'years_of_experience': 8,
        'medical_license_number': 'MLFRONTEND123',
        'state_medical_council': 'Karnataka Medical Council',
        'password1': 'StrongPassword@123',
        'password2': 'StrongPassword@123',
    }
    
    print(f"\n📝 Simulating Frontend Form Data:")
    for key, value in form_data.items():
        if 'password' not in key:
            print(f"   {key}: {value}")
    
    # Create and validate form
    form = DoctorRegistrationForm(data=form_data)
    
    print(f"\n🧪 Form Validation:")
    print(f"   Form is valid: {form.is_valid()}")
    
    if not form.is_valid():
        print(f"   Form errors:")
        for field, errors in form.errors.items():
            print(f"     {field}: {errors}")
        return
    
    # Save the form
    try:
        doctor = form.save()
        print(f"\n✅ Frontend Registration Successful!")
        print(f"   Doctor ID: {doctor.doctor_id}")
        print(f"   Name: {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   Verification Status: {doctor.is_verified}")
        
        # Check if all fields were saved correctly
        fields_correct = all([
            doctor.first_name == 'Frontend',
            doctor.last_name == 'Test',
            doctor.email == 'frontend.test@example.com',
            doctor.phone_number == '9876543299',
            doctor.nmc_registration_number == 'FRONTEND123',
            doctor.specialization == 'GENERAL',
            doctor.hospital_name == 'Frontend Test Hospital',
            doctor.hospital_address == '789 Frontend Street',
            doctor.years_of_experience == 8,
            doctor.medical_license_number == 'MLFRONTEND123',
            doctor.state_medical_council == 'Karnataka Medical Council'
        ])
        print(f"   All fields saved correctly: {fields_correct}")
        
    except Exception as e:
        print(f"❌ Error saving form: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Check if doctor appears in admin dashboard
    print(f"\n📊 Admin Dashboard Check:")
    total_doctors = Doctor.objects.count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    
    print(f"   Total Doctors: {total_doctors}")
    print(f"   Pending Doctors: {pending_doctors}")
    print(f"   Should show in admin: {'Yes' if pending_doctors > 0 else 'No'}")
    
    # List all pending doctors
    print(f"\n📋 Pending Doctors List:")
    for doctor in Doctor.objects.filter(is_verified=False):
        print(f"   - {doctor.first_name} {doctor.last_name} ({doctor.email})")
        print(f"     NMC: {doctor.nmc_registration_number}")
        print(f"     Hospital: {doctor.hospital_name}")

if __name__ == '__main__':
    debug_frontend_registration()
