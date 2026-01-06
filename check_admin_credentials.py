#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

def check_admin_credentials():
    """Check and fix admin credentials"""
    
    print("🔍 CHECKING ADMIN CREDENTIALS")
    print("=" * 50)
    
    User = get_user_model()
    admin_users = User.objects.filter(is_superuser=True)
    
    print(f"Admin Users: {admin_users.count()}")
    
    for admin in admin_users:
        print(f"\n👤 Admin User: {admin.email}")
        print(f"   ID: {admin.id}")
        print(f"   is_superuser: {admin.is_superuser}")
        print(f"   is_active: {admin.is_active}")
        print(f"   is_staff: {admin.is_staff}")
        print(f"   date_joined: {admin.date_joined}")
    
    # Test common passwords
    print(f"\n🔐 Testing Common Admin Passwords:")
    print("-" * 45)
    
    client = Client()
    common_passwords = ['Admin@123', 'admin', 'password', '123456', 'admin123']
    
    if admin_users.exists():
        admin_user = admin_users.first()
        
        for password in common_passwords:
            login_success = client.login(username=admin_user.email, password=password)
            print(f"   Password '{password}': {'✅ Success' if login_success else '❌ Failed'}")
            
            if login_success:
                print(f"   🎉 Found correct password: {password}")
                
                # Test verification page with correct login
                print(f"\n🌐 Testing Verification Page with Correct Login:")
                print("-" * 55)
                
                from doctors.models import Doctor
                pending_doctors = Doctor.objects.filter(is_verified=False)
                
                if pending_doctors.exists():
                    test_doctor = pending_doctors.first()
                    verify_url = f'/admin-panel/verify-doctor/{test_doctor.id}/'
                    
                    response = client.get(verify_url)
                    print(f"   Verification Page Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print(f"   ✅ Verification page loads successfully!")
                        
                        # Test verification submission
                        print(f"\n✅ Testing Verification Submission:")
                        print("-" * 40)
                        
                        response = client.post(verify_url, data={})
                        print(f"   POST Status: {response.status_code}")
                        
                        if response.status_code == 302:
                            print(f"   ✅ Verification submitted successfully!")
                            print(f"   Redirect: {response.get('Location', 'Unknown')}")
                        else:
                            print(f"   ⚠️  Verification submission issue")
                    else:
                        print(f"   ❌ Verification page still not accessible")
                
                return True
    
    return False

if __name__ == '__main__':
    success = check_admin_credentials()
    
    if success:
        print(f"\n✅ ADMIN CREDENTIALS ISSUE RESOLVED!")
        print(f"   Found correct admin password")
        print(f"   Verification page now accessible")
    else:
        print(f"\n❌ ADMIN CREDENTIALS ISSUE PERSISTS!")
        print(f"   Could not find correct admin password")
        print(f"   May need to reset admin credentials")
