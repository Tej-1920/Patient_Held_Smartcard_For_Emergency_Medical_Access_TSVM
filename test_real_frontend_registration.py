#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.forms import DoctorRegistrationForm
from doctors.models import Doctor

def test_real_frontend_registration():
    """Test real frontend registration with typical user data"""
    
    print("🧪 Testing Real Frontend Registration...")
    
    # Clear existing test doctors
    Doctor.objects.filter(email__contains='test').delete()
    
    # Simulate real frontend form data (what a real user would enter)
    form_data = {
        'first_name': 'Rahul',
        'last_name': 'Kumar',
        'email': 'rahul.kumar@example.com',
        'phone_number': '9876543210',
        'nmc_registration_number': 'NMC2024001',
        'specialization': 'GENERAL',
        'hospital_name': 'Apollo Hospital',
        'hospital_address': 'Hyderabad, Telangana',
        'years_of_experience': 5,
        'medical_license_number': 'ML2024001',
        'state_medical_council': 'Andhra Pradesh Medical Council',
        'password1': 'Rahul@123456',
        'password2': 'Rahul@123456',
    }
    
    print(f"\n📝 Real User Form Data:")
    print(f"   Name: {form_data['first_name']} {form_data['last_name']}")
    print(f"   Email: {form_data['email']}")
    print(f"   Phone: {form_data['phone_number']}")
    print(f"   NMC: {form_data['nmc_registration_number']}")
    print(f"   Specialization: {form_data['specialization']}")
    print(f"   Hospital: {form_data['hospital_name']}")
    print(f"   Experience: {form_data['years_of_experience']} years")
    print(f"   License: {form_data['medical_license_number']}")
    print(f"   Council: {form_data['state_medical_council']}")
    
    # Create form exactly like the frontend would
    form = DoctorRegistrationForm(data=form_data)
    
    print(f"\n🔍 Form Validation:")
    print(f"   Is Valid: {form.is_valid()}")
    
    if not form.is_valid():
        print(f"   ❌ Form Errors:")
        for field, errors in form.errors.items():
            print(f"     {field}: {errors}")
        return False
    
    # Save the form
    try:
        doctor = form.save()
        print(f"\n✅ Registration Successful!")
        print(f"   Doctor ID: {doctor.doctor_id}")
        print(f"   Name: Dr. {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   Phone: {doctor.phone_number}")
        print(f"   NMC: {doctor.nmc_registration_number}")
        print(f"   Hospital: {doctor.hospital_name}")
        print(f"   Experience: {doctor.years_of_experience} years")
        print(f"   License: {doctor.medical_license_number}")
        print(f"   Council: {doctor.state_medical_council}")
        print(f"   Verification Status: {'Pending' if not doctor.is_verified else 'Verified'}")
        
        # Check if appears in admin
        print(f"\n📊 Admin Dashboard Check:")
        pending_count = Doctor.objects.filter(is_verified=False).count()
        print(f"   Pending Doctors: {pending_count}")
        print(f"   Should show in admin: {'Yes' if pending_count > 0 else 'No'}")
        
        # Show all pending doctors
        print(f"\n📋 All Pending Doctors:")
        for doc in Doctor.objects.filter(is_verified=False):
            print(f"   - Dr. {doc.first_name} {doc.last_name}")
            print(f"     Email: {doc.email}")
            print(f"     NMC: {doc.nmc_registration_number}")
            print(f"     Hospital: {doc.hospital_name}")
            print(f"     Status: Pending")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_real_frontend_registration()
    if success:
        print(f"\n🎉 Frontend registration test PASSED!")
        print(f"   ✅ Doctor created successfully")
        print(f"   ✅ Should appear in admin panel")
        print(f"   ✅ Ready for admin verification")
    else:
        print(f"\n❌ Frontend registration test FAILED!")
