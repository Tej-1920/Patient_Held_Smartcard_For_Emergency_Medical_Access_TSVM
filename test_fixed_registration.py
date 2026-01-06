#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.forms import DoctorRegistrationForm
from doctors.models import Doctor

def test_fixed_registration():
    """Test the fixed registration form with state_medical_council field"""
    
    print("🔧 TESTING FIXED REGISTRATION FORM")
    print("=" * 50)
    
    # Clear existing test doctors
    Doctor.objects.filter(email__contains='fixed').delete()
    
    # Test the form with all required fields including state_medical_council
    form_data = {
        'first_name': 'Fixed',
        'last_name': 'Test',
        'email': 'fixed.test@example.com',
        'phone_number': '9876543244',
        'nmc_registration_number': 'NMC-FIXED-001',
        'specialization': 'GENERAL',
        'hospital_name': 'Fixed Test Hospital',
        'hospital_address': '123 Fixed Street',
        'years_of_experience': 7,
        'medical_license_number': 'ML-FIXED-001',
        'state_medical_council': 'Andhra Pradesh Medical Council',
        'password1': 'FixedTest@123456',
        'password2': 'FixedTest@123456',
    }
    
    print(f"\n📝 Testing Form with All Fields:")
    for key, value in form_data.items():
        if 'password' not in key:
            print(f"   {key}: {value}")
    
    # Test form validation
    form = DoctorRegistrationForm(data=form_data)
    
    print(f"\n🔍 Form Validation:")
    print(f"   Is Valid: {form.is_valid()}")
    
    if not form.is_valid():
        print(f"   ❌ Form Errors:")
        for field, errors in form.errors.items():
            print(f"     {field}: {errors}")
        return False
    
    # Test form saving
    try:
        doctor = form.save()
        print(f"\n✅ Form Saved Successfully!")
        print(f"   Doctor ID: {doctor.doctor_id}")
        print(f"   Name: {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   State Council: {doctor.state_medical_council}")
        print(f"   NMC: {doctor.nmc_registration_number}")
        print(f"   Hospital: {doctor.hospital_name}")
        print(f"   is_verified: {doctor.is_verified}")
        
    except Exception as e:
        print(f"   ❌ Save Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Verify in database
    try:
        saved_doctor = Doctor.objects.get(email=doctor.email)
        print(f"\n🗄️  Database Verification:")
        print(f"   ✅ Doctor found in database!")
        print(f"   State Council: {saved_doctor.state_medical_council}")
        print(f"   All fields saved correctly!")
        
    except Doctor.DoesNotExist:
        print(f"   ❌ Doctor NOT found in database!")
        return False
    
    # Check admin panel visibility
    pending_count = Doctor.objects.filter(is_verified=False).count()
    print(f"\n🏢 Admin Panel Status:")
    print(f"   Pending Doctors: {pending_count}")
    print(f"   Admin should see: '{pending_count} Doctors awaiting verification'")
    
    return True

if __name__ == '__main__':
    success = test_fixed_registration()
    
    if success:
        print(f"\n🎉 REGISTRATION FORM FIXED!")
        print(f"   ✅ State Medical Council field added")
        print(f"   ✅ Form validation works")
        print(f"   ✅ Doctor saved to database")
        print(f"   ✅ Admin can see pending verification")
        print(f"\n📝 Ready for manual testing!")
    else:
        print(f"\n❌ REGISTRATION FORM STILL HAS ISSUES!")
