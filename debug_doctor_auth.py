#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from django.test import Client
from django.urls import reverse

def debug_doctor_auth():
    """Debug doctor authentication issues"""
    
    print("🔍 DEBUGGING DOCTOR AUTHENTICATION")
    print("=" * 50)
    
    # Get doctor details
    doctor = Doctor.objects.filter(is_verified=True).first()
    
    if not doctor:
        print("❌ No verified doctors found")
        return
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Email: {doctor.email}")
    print(f"Doctor ID: {doctor.doctor_id}")
    print(f"Verified: {doctor.is_verified}")
    print(f"Has Password: {'Yes' if doctor.password else 'No'}")
    
    # Test password check
    print(f"\n🔑 Testing Password Check:")
    print("-" * 30)
    
    test_passwords = ['doctor123', 'password123', 'admin']
    
    for pwd in test_passwords:
        try:
            is_valid = doctor.check_password(pwd)
            print(f"Password '{pwd}': {'✅ Valid' if is_valid else '❌ Invalid'}")
        except Exception as e:
            print(f"Password '{pwd}': ❌ Error - {e}")
    
    # Set a known password
    print(f"\n🔧 Setting Known Password:")
    print("-" * 30)
    
    doctor.set_password('doctor123')
    doctor.save()
    print("✅ Password set to 'doctor123'")
    
    # Test password again
    is_valid = doctor.check_password('doctor123')
    print(f"Password check: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # Test login process manually
    print(f"\n🌐 Testing Login Process:")
    print("-" * 35)
    
    client = Client()
    login_url = reverse('doctors:login')
    
    # Test GET request
    response = client.get(login_url)
    print(f"GET Login Page: {response.status_code}")
    
    # Test POST request
    response = client.post(login_url, {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    print(f"POST Login: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Login successful (redirect)")
        print(f"Redirect to: {response.url}")
    elif response.status_code == 200:
        print("❌ Login failed - returned to login page")
        
        # Check for messages
        content = response.content.decode('utf-8')
        if 'messages' in content:
            print("Messages found in response")
        
        # Check session for messages
        from django.contrib.messages import get_messages
        messages = list(get_messages(response.wsgi_request))
        if messages:
            for message in messages:
                print(f"Message: {message.tags} - {message.message}")
        else:
            print("No messages found")
    
    # Test direct login function
    print(f"\n🧪 Testing Direct Login:")
    print("-" * 35)
    
    try:
        from django.contrib.auth import login
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.post('/login/')
        request.user = doctor
        
        # Simulate login
        login(request, doctor)
        print("✅ Direct login successful")
        print(f"User in request: {request.user}")
        print(f"Is authenticated: {request.user.is_authenticated}")
        
    except Exception as e:
        print(f"❌ Direct login failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_doctor_auth()
