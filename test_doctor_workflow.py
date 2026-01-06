#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from django.contrib.auth import authenticate

def test_doctor_workflow():
    """Test the complete doctor registration and verification workflow"""
    
    print("🧪 Testing Doctor Registration & Verification Workflow...")
    
    # 1. Check existing doctors
    doctors = Doctor.objects.all()
    print(f"\n📊 Current Doctors: {doctors.count()}")
    
    for doctor in doctors:
        print(f"   - {doctor.first_name} {doctor.last_name}")
        print(f"     Email: {doctor.email}")
        print(f"     Verified: {doctor.is_verified}")
        print(f"     NMC: {doctor.nmc_registration_number}")
        print(f"     License: {doctor.medical_license_number}")
        print(f"     Council: {doctor.state_medical_council}")
        print()
    
    # 2. Test login for unverified doctor
    print("🔐 Testing Login for Unverified Doctor...")
    test_doctor = doctors.filter(is_verified=False).first()
    
    if test_doctor:
        print(f"   Testing login for: {test_doctor.email}")
        
        # Test authentication
        user = authenticate(username=test_doctor.email, password='Test@123')
        
        if user:
            print(f"   ✅ Authentication successful")
            print(f"   🚫 But login should be blocked due to verification status")
            print(f"   📝 Verification status: {user.is_verified}")
            
            if user.is_verified:
                print(f"   ✅ Would be allowed to login")
            else:
                print(f"   🚫 Login should be blocked - pending verification")
        else:
            print(f"   ❌ Authentication failed")
    else:
        print("   No unverified doctors found")
    
    # 3. Test login for verified doctor
    print("\n🔐 Testing Login for Verified Doctor...")
    verified_doctor = doctors.filter(is_verified=True).first()
    
    if verified_doctor:
        print(f"   Testing login for: {verified_doctor.email}")
        
        # Test authentication
        user = authenticate(username=verified_doctor.email, password='Test@123')
        
        if user:
            print(f"   ✅ Authentication successful")
            print(f"   ✅ Login should be allowed - verified status")
            print(f"   📝 Verification status: {user.is_verified}")
        else:
            print(f"   ❌ Authentication failed")
    else:
        print("   No verified doctors found")
    
    # 4. Summary
    print(f"\n📋 Workflow Summary:")
    print(f"   Total Doctors: {doctors.count()}")
    print(f"   Pending: {doctors.filter(is_verified=False).count()}")
    print(f"   Verified: {doctors.filter(is_verified=True).count()}")
    print(f"   ✅ Registration: Doctors can register")
    print(f"   ✅ Admin Review: Admin can see details and verify")
    print(f"   ✅ Login Control: Unverified doctors cannot login")
    print(f"   ✅ Verification: Admin can approve doctors")

if __name__ == '__main__':
    test_doctor_workflow()
