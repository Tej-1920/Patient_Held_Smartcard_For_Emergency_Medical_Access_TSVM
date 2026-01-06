#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.forms import DoctorRegistrationForm

def test_doctor_registration():
    """Test doctor registration form"""
    
    print("🧪 Testing Doctor Registration Form...")
    
    # Test data
    form_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe.test@example.com',
        'phone_number': '9876543211',
        'nmc_registration_number': 'TEST789012',
        'specialization': 'GENERAL',
        'hospital_name': 'Test Hospital',
        'hospital_address': '123 Test Street',
        'years_of_experience': 10,
        'medical_license_number': 'ML789012',
        'state_medical_council': 'Andhra Pradesh Medical Council',
        'password1': 'Test@123456',
        'password2': 'Test@123456',
    }
    
    # Create form
    form = DoctorRegistrationForm(data=form_data)
    
    # Check if valid
    if form.is_valid():
        print("✅ Form is valid!")
        
        try:
            # Save the doctor
            doctor = form.save()
            print(f"✅ Doctor created successfully!")
            print(f"   Name: Dr. {doctor.first_name} {doctor.last_name}")
            print(f"   Email: {doctor.email}")
            print(f"   Doctor ID: {doctor.doctor_id}")
            print(f"   Verification Status: {'Verified' if doctor.is_verified else 'Pending'}")
            print(f"   Specialization: {doctor.get_specialization_display()}")
            print(f"   Hospital: {doctor.hospital_name}")
            print(f"   State Council: {doctor.state_medical_council}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving doctor: {e}")
            return False
    else:
        print("❌ Form is invalid!")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
        return False

if __name__ == '__main__':
    success = test_doctor_registration()
    if success:
        print("\n🎉 Doctor registration test completed successfully!")
        print("   The doctor should now appear in admin panel pending verification.")
    else:
        print("\n❌ Doctor registration test failed!")
