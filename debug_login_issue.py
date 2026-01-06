#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.contrib.auth import authenticate
from doctors.models import Doctor

def debug_login_issue():
    """Debug the login issue"""
    
    print("🔍 Debugging Login Issue...")
    
    # Check all doctors
    doctors = Doctor.objects.all()
    print(f"\n📊 Total Doctors: {doctors.count()}")
    
    for doctor in doctors:
        print(f"\n👨‍⚕️ Doctor: {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   is_verified: {doctor.is_verified}")
        print(f"   is_active: {doctor.is_active}")
        print(f"   is_staff: {doctor.is_staff}")
        print(f"   is_superuser: {doctor.is_superuser}")
        
        # Test authentication with different methods
        print(f"\n🔐 Testing Authentication:")
        
        # Method 1: Using email as username
        user1 = authenticate(username=doctor.email, password='Test@123')
        print(f"   Method 1 (email as username): {user1 is not None}")
        
        # Method 2: Using actual username
        if doctor.username:
            user2 = authenticate(username=doctor.username, password='Test@123')
            print(f"   Method 2 (actual username): {user2 is not None}")
        
        # Method 3: Check password directly
        print(f"   Password check: {doctor.check_password('Test@123')}")
        
        # Check if the user object is the same
        if user1:
            print(f"   Authenticated user type: {type(user1)}")
            print(f"   Is Doctor instance: {isinstance(user1, Doctor)}")
            print(f"   User is_verified: {getattr(user1, 'is_verified', 'N/A')}")
    
    # Test the specific login logic
    print(f"\n🧪 Testing Login Logic:")
    
    test_doctor = doctors.first()
    if test_doctor:
        print(f"   Testing with: {test_doctor.email}")
        
        # Simulate the login view logic
        email = test_doctor.email
        password = 'Test@123'
        user = authenticate(request=None, username=email, password=password)
        
        if user is not None:
            print(f"   ✅ User authenticated: {user}")
            
            # Check the verification logic
            if hasattr(user, 'doctor') or isinstance(user, Doctor):
                print(f"   ✅ User is doctor type")
                
                if user.is_verified:
                    print(f"   ✅ User is verified - would allow login")
                else:
                    print(f"   🚫 User not verified - would block login")
            else:
                print(f"   ❌ User is not doctor type")
        else:
            print(f"   ❌ Authentication failed")

if __name__ == '__main__':
    debug_login_issue()
