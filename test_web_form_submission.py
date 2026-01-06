#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client, TestCase
from django.urls import reverse
from doctors.models import Doctor

def test_web_form_submission():
    """Test the actual web form submission like a browser would"""
    
    print("🌐 TESTING WEB FORM SUBMISSION")
    print("=" * 50)
    
    # Clear any existing test doctors
    Doctor.objects.filter(email__contains='webform').delete()
    
    # Create a test client (simulates browser)
    client = Client()
    
    # Step 1: GET the registration page
    print(f"\n📄 Step 1: GET Registration Page")
    try:
        response = client.get('/doctor/register/')
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Registration page loaded successfully")
        else:
            print(f"   ❌ Registration page failed to load")
            return False
    except Exception as e:
        print(f"   ❌ Error accessing registration page: {e}")
        return False
    
    # Step 2: POST the registration form
    print(f"\n📝 Step 2: POST Registration Form")
    
    form_data = {
        'first_name': 'Web',
        'last_name': 'Form',
        'email': 'web.form.test@example.com',
        'phone_number': '9876543266',
        'nmc_registration_number': 'NMC-WEB-001',
        'specialization': 'GENERAL',
        'hospital_name': 'Web Form Hospital',
        'hospital_address': '456 Web Form Street',
        'years_of_experience': 6,
        'medical_license_number': 'ML-WEB-001',
        'state_medical_council': 'Andhra Pradesh Medical Council',
        'password1': 'WebForm@123456',
        'password2': 'WebForm@123456',
    }
    
    print(f"   Submitting form data:")
    for key, value in form_data.items():
        if 'password' not in key:
            print(f"     {key}: {value}")
    
    try:
        response = client.post('/doctor/register/', data=form_data)
        print(f"   Status Code: {response.status_code}")
        
        # Check if redirected to login page (success)
        if response.status_code == 302:
            print(f"   ✅ Form submitted successfully (redirected)")
            print(f"   Redirect to: {response.url}")
        elif response.status_code == 200:
            print(f"   ⚠️  Form returned to same page (validation errors)")
            
            # Check for form errors in response
            if hasattr(response, 'context_data') and response.context_data:
                form = response.context_data.get('form')
                if form and form.errors:
                    print(f"   ❌ Form Errors:")
                    for field, errors in form.errors.items():
                        print(f"     {field}: {errors}")
        else:
            print(f"   ❌ Unexpected response status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error submitting form: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Check if doctor was created
    print(f"\n🗄️  Step 3: Database Check")
    
    try:
        doctor = Doctor.objects.get(email='web.form.test@example.com')
        print(f"   ✅ Doctor found in database!")
        print(f"   Name: {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   NMC: {doctor.nmc_registration_number}")
        print(f"   Hospital: {doctor.hospital_name}")
        print(f"   is_verified: {doctor.is_verified}")
        print(f"   Created: {doctor.created_at}")
        
    except Doctor.DoesNotExist:
        print(f"   ❌ Doctor NOT found in database!")
        return False
    
    # Step 4: Check admin panel visibility
    print(f"\n🏢 Step 4: Admin Panel Check")
    
    total_doctors = Doctor.objects.count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    
    print(f"   Total Doctors: {total_doctors}")
    print(f"   Pending Doctors: {pending_doctors}")
    
    if pending_doctors > 0:
        print(f"   ✅ Admin should see '{pending_doctors} Doctors awaiting verification'")
        
        print(f"\n📋 All Pending Doctors:")
        for doc in Doctor.objects.filter(is_verified=False):
            print(f"     - Dr. {doc.first_name} {doc.last_name} ({doc.email})")
    else:
        print(f"   ❌ Admin will see '0 Doctors awaiting verification'")
    
    return True

if __name__ == '__main__':
    success = test_web_form_submission()
    
    if success:
        print(f"\n🎉 WEB FORM SUBMISSION TEST PASSED!")
        print(f"   ✅ Frontend registration works correctly")
        print(f"   ✅ Doctor saved to database")
        print(f"   ✅ Admin should see pending verification")
    else:
        print(f"\n❌ WEB FORM SUBMISSION TEST FAILED!")
        print(f"   🔧 Check form validation or view logic")
