#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor

def manual_testing_guide():
    """Provide a manual testing guide for the complete workflow"""
    
    print("🎯 MANUAL TESTING GUIDE - Complete Doctor Workflow")
    print("=" * 60)
    
    print(f"\n📋 STEP-BY-STEP TESTING INSTRUCTIONS:")
    print("=" * 40)
    
    print(f"\n🔹 STEP 1: DOCTOR REGISTRATION")
    print("-" * 30)
    print(f"1. Open browser and go to: http://127.0.0.1:8000/doctor/register/")
    print(f"2. Fill the registration form with:")
    print(f"   First Name: Test")
    print(f"   Last Name: Doctor")
    print(f"   Email: test.doctor.manual@example.com")
    print(f"   Phone: 9876543288")
    print(f"   NMC Registration: MANUAL-TEST-001")
    print(f"   Specialization: General Practitioner")
    print(f"   Hospital: Manual Test Hospital")
    print(f"   Hospital Address: 123 Test Street")
    print(f"   Years of Experience: 3")
    print(f"   Medical License: ML-MANUAL-001")
    print(f"   State Medical Council: Andhra Pradesh Medical Council")
    print(f"   Password: TestDoctor@123456")
    print(f"   Confirm Password: TestDoctor@123456")
    print(f"3. Click 'Register' button")
    print(f"4. EXPECTED: 'Registration successful! Your account is pending verification'")
    
    print(f"\n🔹 STEP 2: ADMIN VERIFICATION")
    print("-" * 30)
    print(f"1. Open new tab and go to: http://127.0.0.1:8000/admin-panel/login/")
    print(f"2. Login with:")
    print(f"   Email: admin@patientsmartcard.com")
    print(f"   Password: Admin@123")
    print(f"3. EXPECTED: Admin dashboard shows 'X Doctors awaiting verification'")
    print(f"4. Click 'Review Applications' button")
    print(f"5. EXPECTED: See the newly registered doctor with all details")
    print(f"6. Click green 'Verify' button next to the doctor")
    print(f"7. EXPECTED: 'Doctor [Name] has been verified successfully'")
    
    print(f"\n🔹 STEP 3: DOCTOR LOGIN (AFTER VERIFICATION)")
    print("-" * 30)
    print(f"1. Go to: http://127.0.0.1:8000/doctor/login/")
    print(f"2. Login with:")
    print(f"   Email: test.doctor.manual@example.com")
    print(f"   Password: TestDoctor@123456")
    print(f"3. EXPECTED: 'Login successful!' → Redirect to doctor dashboard")
    
    print(f"\n🔹 STEP 4: DOCTOR LOGIN (BEFORE VERIFICATION)")
    print("-" * 30)
    print(f"1. Register a new doctor (different email)")
    print(f"2. Try to login immediately after registration")
    print(f"3. EXPECTED: 'Your account is pending verification. Please wait for admin approval.'")
    
    print(f"\n📊 CURRENT SYSTEM STATUS:")
    print("-" * 30)
    
    total_doctors = Doctor.objects.count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    verified_doctors = Doctor.objects.filter(is_verified=True).count()
    
    print(f"Total Doctors: {total_doctors}")
    print(f"Pending Verification: {pending_doctors}")
    print(f"Verified: {verified_doctors}")
    
    if pending_doctors > 0:
        print(f"\n📋 PENDING DOCTORS FOR ADMIN REVIEW:")
        for doctor in Doctor.objects.filter(is_verified=False):
            print(f"   - Dr. {doctor.first_name} {doctor.last_name}")
            print(f"     Email: {doctor.email}")
            print(f"     NMC: {doctor.nmc_registration_number}")
            print(f"     Hospital: {doctor.hospital_name}")
    
    print(f"\n✅ EXPECTED RESULTS:")
    print("-" * 30)
    print(f"• Registration form creates doctor with 'pending' status")
    print(f"• Admin dashboard shows pending doctors count")
    print(f"• Admin can see all registration details")
    print(f"• Admin can verify doctors with one click")
    print(f"• Unverified doctors cannot login")
    print(f"• Verified doctors can login and access dashboard")
    
    print(f"\n🔧 TROUBLESHOOTING:")
    print("-" * 30)
    print(f"• If registration fails: Check password strength (use strong, unique password)")
    print(f"• If admin doesn't see pending: Refresh admin dashboard")
    print(f"• If login doesn't work: Check email and password exactly")
    print(f"• If verification doesn't work: Check admin permissions")

if __name__ == '__main__':
    manual_testing_guide()
