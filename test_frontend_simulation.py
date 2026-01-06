#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.forms import DoctorRegistrationForm
from doctors.models import Doctor

def test_frontend_simulation():
    """Simulate exact frontend registration process"""
    
    print("🧪 SIMULATING FRONTEND REGISTRATION")
    print("=" * 50)
    
    # Clear any existing test doctors
    Doctor.objects.filter(email__contains='frontend').delete()
    
    # Simulate the exact data from your frontend form
    frontend_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe.frontend@example.com',
        'phone_number': '9876543277',
        'nmc_registration_number': 'NMC-FRONTEND-001',
        'specialization': 'GENERAL',
        'hospital_name': 'Frontend Test Hospital',
        'hospital_address': '123 Frontend Street',
        'years_of_experience': 5,
        'medical_license_number': 'ML-FRONTEND-001',
        'state_medical_council': 'Andhra Pradesh Medical Council',
        'password1': 'JohnDoe@123456',
        'password2': 'JohnDoe@123456',
    }
    
    print(f"\n📝 Frontend Form Data:")
    for key, value in frontend_data.items():
        if 'password' not in key:
            print(f"   {key}: {value}")
    
    # Step 1: Create form like the frontend does
    print(f"\n🔍 Step 1: Form Creation & Validation")
    form = DoctorRegistrationForm(data=frontend_data)
    
    print(f"   Form is valid: {form.is_valid()}")
    
    if not form.is_valid():
        print(f"   ❌ Form Errors:")
        for field, errors in form.errors.items():
            print(f"     {field}: {errors}")
        return False
    
    # Step 2: Try to save the form
    print(f"\n💾 Step 2: Form Saving")
    try:
        doctor = form.save()
        print(f"   ✅ Form saved successfully!")
        print(f"   Doctor ID: {doctor.doctor_id}")
        print(f"   Name: {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   is_verified: {doctor.is_verified}")
        
    except Exception as e:
        print(f"   ❌ Form save failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Verify doctor is in database
    print(f"\n🗄️  Step 3: Database Verification")
    
    try:
        saved_doctor = Doctor.objects.get(email=doctor.email)
        print(f"   ✅ Doctor found in database!")
        print(f"   ID: {saved_doctor.doctor_id}")
        print(f"   Name: {saved_doctor.first_name} {saved_doctor.last_name}")
        print(f"   Email: {saved_doctor.email}")
        print(f"   Phone: {saved_doctor.phone_number}")
        print(f"   NMC: {saved_doctor.nmc_registration_number}")
        print(f"   Hospital: {saved_doctor.hospital_name}")
        print(f"   is_verified: {saved_doctor.is_verified}")
        print(f"   Created: {saved_doctor.created_at}")
        
    except Doctor.DoesNotExist:
        print(f"   ❌ Doctor NOT found in database!")
        return False
    
    # Step 4: Check admin panel visibility
    print(f"\n🏢 Step 4: Admin Panel Check")
    
    total_doctors = Doctor.objects.count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    
    print(f"   Total Doctors: {total_doctors}")
    print(f"   Pending Doctors: {pending_doctors}")
    
    if pending_doctors > 0:
        print(f"   ✅ Admin should see '{pending_doctors} Doctors awaiting verification'")
        
        print(f"\n📋 Pending Doctors List:")
        for doc in Doctor.objects.filter(is_verified=False):
            print(f"     - Dr. {doc.first_name} {doc.last_name} ({doc.email})")
    else:
        print(f"   ❌ Admin will see '0 Doctors awaiting verification'")
    
    return True

if __name__ == '__main__':
    success = test_frontend_simulation()
    
    if success:
        print(f"\n🎉 FRONTEND SIMULATION SUCCESS!")
        print(f"   ✅ Registration process works correctly")
        print(f"   ✅ Doctor saved to database")
        print(f"   ✅ Admin should see pending verification")
    else:
        print(f"\n❌ FRONTEND SIMULATION FAILED!")
        print(f"   🔧 Check form validation or database saving")
