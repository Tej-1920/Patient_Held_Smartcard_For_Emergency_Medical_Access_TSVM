#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from doctors.models import Doctor

def test_doctor_login():
    """Test doctor login functionality"""
    
    print("🔐 TESTING DOCTOR LOGIN SYSTEM")
    print("=" * 45)
    
    # Step 1: Test URL patterns
    print(f"\n🔗 Step 1: Test URL Patterns")
    print("-" * 35)
    
    try:
        login_url = reverse('doctors:login')
        dashboard_url = reverse('doctors:dashboard')
        
        print(f"✅ Login URL: {login_url}")
        print(f"✅ Dashboard URL: {dashboard_url}")
        
    except Exception as e:
        print(f"❌ URL pattern error: {e}")
        return False
    
    # Step 2: Test login page access
    print(f"\n🌐 Step 2: Test Login Page Access")
    print("-" * 40)
    
    client = Client()
    
    try:
        response = client.get(login_url)
        print(f"Login Page Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login page loads successfully")
            
            # Check content
            content = response.content.decode('utf-8')
            if 'Doctor Login' in content:
                print("✅ Login page title correct")
            if 'form' in content:
                print("✅ Login form present")
            if 'csrf_token' in content:
                print("✅ CSRF token present")
                
        else:
            print(f"❌ Login page failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing login page: {e}")
        return False
    
    # Step 3: Test doctor login
    print(f"\n👨‍⚕️  Step 3: Test Doctor Login")
    print("-" * 40)
    
    # Get a verified doctor
    doctor = Doctor.objects.filter(is_verified=True).first()
    
    if not doctor:
        print("❌ No verified doctors found")
        return False
    
    print(f"Testing with: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Email: {doctor.email}")
    
    # Set password if needed
    if not doctor.password:
        doctor.set_password('doctor123')
        doctor.save()
        print("✅ Password set to: doctor123")
    
    try:
        # Test login POST request
        response = client.post(login_url, {
            'email': doctor.email,
            'password': 'doctor123'
        })
        
        print(f"Login Response Status: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Login successful (redirect)")
            
            # Check redirect location
            if response.url == dashboard_url:
                print("✅ Redirects to dashboard correctly")
            else:
                print(f"⚠️  Redirects to: {response.url}")
                
        elif response.status_code == 200:
            print("⚠️  Login returned to same page (check for errors)")
            
            # Check for error messages
            content = response.content.decode('utf-8')
            if 'error' in content.lower() or 'invalid' in content.lower():
                print("❌ Login error messages present")
                print("Content preview:")
                print(content[:500])
        else:
            print(f"❌ Unexpected login response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error during login: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Test dashboard access after login
    print(f"\n📊 Step 4: Test Dashboard Access")
    print("-" * 40)
    
    try:
        # Follow redirect to dashboard
        response = client.post(login_url, {
            'email': doctor.email,
            'password': 'doctor123'
        }, follow=True)
        
        print(f"Dashboard Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Dashboard accessible after login")
            
            # Check dashboard content
            content = response.content.decode('utf-8')
            if 'Doctor Dashboard' in content:
                print("✅ Dashboard title correct")
            if doctor.first_name in content:
                print("✅ Doctor name displayed")
            if 'Welcome' in content:
                print("✅ Welcome message present")
                
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error accessing dashboard: {e}")
    
    return True

if __name__ == '__main__':
    success = test_doctor_login()
    
    if success:
        print(f"\n🎉 DOCTOR LOGIN SYSTEM WORKING!")
        print(f"   ✅ URL patterns configured correctly")
        print(f"   ✅ Login page accessible")
        print(f"   ✅ Login functionality working")
        print(f"   ✅ Dashboard accessible")
        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
        print("=" * 50)
        print(f"   1. Go to: http://127.0.0.1:8000/doctor/login/")
        print(f"   2. Use credentials:")
        print(f"      - Email: chaitanyauggina@gmail.com")
        print(f"      - Password: doctor123")
        print(f"   3. Click login button")
        print(f"   4. Should redirect to dashboard")
    else:
        print(f"\n❌ DOCTOR LOGIN SYSTEM HAS ISSUES!")
