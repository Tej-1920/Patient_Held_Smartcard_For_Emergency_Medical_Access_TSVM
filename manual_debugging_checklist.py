#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor

def manual_debugging_checklist():
    """Provide a comprehensive checklist for manual debugging"""
    
    print("🔍 MANUAL DEBUGGING CHECKLIST")
    print("=" * 50)
    
    print(f"\n📊 CURRENT DATABASE STATUS:")
    print("-" * 30)
    
    total_doctors = Doctor.objects.count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    verified_doctors = Doctor.objects.filter(is_verified=True).count()
    
    print(f"Total Doctors: {total_doctors}")
    print(f"Pending Verification: {pending_doctors}")
    print(f"Verified: {verified_doctors}")
    
    if pending_doctors > 0:
        print(f"\n📋 CURRENT PENDING DOCTORS:")
        for doctor in Doctor.objects.filter(is_verified=False):
            print(f"   - Dr. {doctor.first_name} {doctor.last_name}")
            print(f"     Email: {doctor.email}")
            print(f"     NMC: {doctor.nmc_registration_number}")
            print(f"     Hospital: {doctor.hospital_name}")
            print(f"     Created: {doctor.created_at}")
            print(f"     Doctor ID: {doctor.doctor_id}")
    
    print(f"\n🔧 STEP-BY-STEP MANUAL DEBUGGING:")
    print("=" * 40)
    
    print(f"\n1️⃣  BEFORE REGISTRATION:")
    print("-" * 25)
    print(f"   ✅ Check database: Run this script to see current doctors")
    print(f"   ✅ Clear browser cache and cookies")
    print(f"   ✅ Open developer tools (F12)")
    print(f"   ✅ Go to Network tab")
    print(f"   ✅ Clear network log")
    
    print(f"\n2️⃣  DURING REGISTRATION:")
    print("-" * 25)
    print(f"   📝 Fill form with these EXACT values:")
    print(f"      First Name: Manual")
    print(f"      Last Name: Test")
    print(f"      Email: manual.test@example.com")
    print(f"      Phone: 9876543255")
    print(f"      NMC Registration: MANUAL-TEST-001")
    print(f"      Specialization: General Practitioner")
    print(f"      Hospital: Manual Test Hospital")
    print(f"      Hospital Address: 123 Manual Street")
    print(f"      Years of Experience: 4")
    print(f"      Medical License: ML-MANUAL-001")
    print(f"      State Medical Council: Andhra Pradesh Medical Council")
    print(f"      Password: ManualTest@123456")
    print(f"      Confirm Password: ManualTest@123456")
    print(f"   🖱️  Click Register button")
    print(f"   👀 Watch Network tab for POST request")
    print(f"   📸 Take screenshot of success message")
    
    print(f"\n3️⃣  AFTER REGISTRATION:")
    print("-" * 25)
    print(f"   ✅ Check if redirected to login page")
    print(f"   ✅ Note the exact success message")
    print(f"   ✅ Run this script again to check database")
    print(f"   ✅ Check Network tab for response status")
    
    print(f"\n4️⃣  ADMIN PANEL CHECK:")
    print("-" * 25)
    print(f"   🔐 Login to admin: admin@patientsmartcard.com / Admin@123")
    print(f"   📊 Check dashboard for pending count")
    print(f"   🔍 Click 'Review Applications'")
    print(f"   👀 Look for newly registered doctor")
    
    print(f"\n🚨 COMMON ISSUES & SOLUTIONS:")
    print("=" * 40)
    
    print(f"\n❌ ISSUE 1: Form Validation Errors")
    print(f"   Symptoms: Stays on registration page, shows errors")
    print(f"   Solution: Check all required fields, use strong password")
    print(f"   Debug: Look at form error messages")
    
    print(f"\n❌ ISSUE 2: Network/Server Errors")
    print(f"   Symptoms: Page doesn't load, shows server error")
    print(f"   Solution: Check Django server is running")
    print(f"   Debug: Look at Network tab status codes")
    
    print(f"\n❌ ISSUE 3: Silent Failure")
    print(f"   Symptoms: Shows success but doctor not in database")
    print(f"   Solution: Check Django console for errors")
    print(f"   Debug: Look at server logs")
    
    print(f"\n❌ ISSUE 4: Admin Cache")
    print(f"   Symptoms: Doctor exists but admin doesn't see it")
    print(f"   Solution: Refresh admin dashboard")
    print(f"   Debug: Check database directly")
    
    print(f"\n🔍 DEBUGGING TOOLS:")
    print("=" * 40)
    
    print(f"\n1. Browser Developer Tools:")
    print(f"   - F12 → Network tab")
    print(f"   - Watch for POST /doctor/register/")
    print(f"   - Check response status (should be 302)")
    print(f"   - Check response headers")
    
    print(f"\n2. Django Console:")
    print(f"   - Watch server output for errors")
    print(f"   - Look for database save messages")
    print(f"   - Check for exception tracebacks")
    
    print(f"\n3. Database Verification:")
    print(f"   - Run this script before/after registration")
    print(f"   - Compare doctor counts")
    print(f"   - Check new doctor details")
    
    print(f"\n4. Admin Panel:")
    print(f"   - Refresh dashboard after registration")
    print(f"   - Check pending doctor count")
    print(f"   - Look for new doctor in list")
    
    print(f"\n✅ EXPECTED RESULTS:")
    print("=" * 40)
    print(f"   • Form submission: Status 302 (redirect)")
    print(f"   • Success message: 'Registration successful! Your account is pending verification'")
    print(f"   • Database: +1 doctor with is_verified=False")
    print(f"   • Admin panel: Shows increased pending count")
    print(f"   • New doctor: Visible in admin review list")

if __name__ == '__main__':
    manual_debugging_checklist()
