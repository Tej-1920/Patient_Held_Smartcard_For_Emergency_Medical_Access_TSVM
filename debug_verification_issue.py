#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

def debug_verification_issue():
    """Debug the verification page issue"""
    
    print("🔍 DEBUGGING VERIFICATION ISSUE")
    print("=" * 50)
    
    # Step 1: Check admin users
    print(f"\n👤 Step 1: Admin User Check")
    print("-" * 35)
    
    User = get_user_model()
    admin_users = User.objects.filter(is_superuser=True)
    
    print(f"Admin Users: {admin_users.count()}")
    
    for admin in admin_users:
        print(f"   - {admin.email}")
        print(f"     is_superuser: {admin.is_superuser}")
        print(f"     is_active: {admin.is_active}")
        print(f"     is_staff: {admin.is_staff}")
    
    # Step 2: Test admin login
    print(f"\n🔐 Step 2: Admin Login Test")
    print("-" * 35)
    
    client = Client()
    
    if admin_users.exists():
        admin_user = admin_users.first()
        print(f"Testing login with: {admin_user.email}")
        
        # Test login
        login_success = client.login(username=admin_user.email, password='Admin@123')
        print(f"Login Success: {login_success}")
        
        if login_success:
            print(f"✅ Admin login successful")
        else:
            print(f"❌ Admin login failed")
            
            # Try different password
            login_success2 = client.login(username=admin_user.email, password='admin')
            print(f"Login with 'admin': {login_success2}")
    else:
        print(f"❌ No admin users found")
        return False
    
    # Step 3: Test verification URL
    print(f"\n🔗 Step 3: Verification URL Test")
    print("-" * 35)
    
    pending_doctors = Doctor.objects.filter(is_verified=False)
    
    if pending_doctors.exists():
        test_doctor = pending_doctors.first()
        print(f"Testing with doctor: {test_doctor.first_name} {test_doctor.last_name}")
        print(f"Doctor ID: {test_doctor.id}")
        
        # Test the URL
        verify_url = f'/admin-panel/verify-doctor/{test_doctor.id}/'
        print(f"Verification URL: {verify_url}")
        
        # Try to access the URL
        try:
            response = client.get(verify_url)
            print(f"Response Status: {response.status_code}")
            
            if response.status_code == 302:
                print(f"Redirect Location: {response.get('Location', 'Unknown')}")
                
                # Check if it's redirecting to login
                if 'login' in response.get('Location', ''):
                    print(f"❌ Redirecting to login (authentication issue)")
                else:
                    print(f"✅ Redirecting elsewhere (expected behavior)")
                    
            elif response.status_code == 200:
                print(f"✅ Page loads successfully")
            elif response.status_code == 404:
                print(f"❌ Page not found (URL issue)")
            elif response.status_code == 403:
                print(f"❌ Access denied (permission issue)")
            else:
                print(f"⚠️  Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error accessing URL: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ No pending doctors to test")
    
    # Step 4: Check URL patterns
    print(f"\n🛣️  Step 4: URL Pattern Check")
    print("-" * 35)
    
    try:
        from django.urls import reverse
        verify_url_pattern = reverse('admin_panel:verify_doctor', kwargs={'doctor_id': test_doctor.id})
        print(f"Reverse URL: {verify_url_pattern}")
        
        # Check if URL matches expected pattern
        expected_pattern = f'/admin-panel/verify-doctor/{test_doctor.id}/'
        if verify_url_pattern == expected_pattern:
            print(f"✅ URL pattern matches expected")
        else:
            print(f"❌ URL pattern mismatch")
            print(f"   Expected: {expected_pattern}")
            print(f"   Got: {verify_url_pattern}")
            
    except Exception as e:
        print(f"❌ URL reverse error: {e}")
    
    return True

if __name__ == '__main__':
    debug_verification_issue()
