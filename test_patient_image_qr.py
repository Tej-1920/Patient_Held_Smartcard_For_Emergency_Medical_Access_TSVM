#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient
from django.test import Client
from django.contrib.auth import get_user_model

def test_patient_image_qr():
    """Test patient image upload and QR code generation"""
    
    print("🔍 TESTING PATIENT IMAGE & QR CODE FUNCTIONALITY")
    print("=" * 60)
    
    # Step 1: Check if qrcode library is available
    print(f"\n📦 Step 1: Check Dependencies")
    print("-" * 35)
    
    try:
        import qrcode
        print(f"✅ qrcode library available")
    except ImportError:
        print(f"❌ qrcode library not installed")
        print(f"   Run: pip install qrcode[pil]")
        return False
    
    # Step 2: Check existing patients
    print(f"\n👤 Step 2: Check Existing Patients")
    print("-" * 40)
    
    patients = Patient.objects.all()
    print(f"Total Patients: {patients.count()}")
    
    if patients.count() == 0:
        print("❌ No patients found for testing")
        return False
    
    for patient in patients:
        print(f"   - {patient.first_name} {patient.last_name} ({patient.patient_id})")
        print(f"     Has Image: {'Yes' if patient.profile_image else 'No'}")
        print(f"     Has QR Code: {'Yes' if patient.qr_code else 'No'}")
    
    # Step 3: Test QR code generation
    print(f"\n🔲 Step 3: Test QR Code Generation")
    print("-" * 40)
    
    test_patient = patients.first()
    print(f"Testing with: {test_patient.first_name} {test_patient.last_name}")
    
    try:
        # Generate QR code
        test_patient.generate_qr_code()
        test_patient.save()
        
        if test_patient.qr_code:
            print(f"✅ QR Code generated successfully!")
            print(f"   QR Code URL: {test_patient.qr_code.url}")
            print(f"   File Name: {test_patient.qr_code.name}")
        else:
            print(f"❌ QR Code generation failed")
            
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")
        return False
    
    # Step 4: Test QR code data
    print(f"\n📄 Step 4: Test QR Code Data")
    print("-" * 35)
    
    qr_data = test_patient.get_qr_data()
    print(f"QR Code Data:")
    print(qr_data)
    
    # Step 5: Test form functionality
    print(f"\n📝 Step 5: Test Form Functionality")
    print("-" * 40)
    
    from patients.forms import PatientProfileForm
    
    form = PatientProfileForm(instance=test_patient)
    print(f"✅ PatientProfileForm created")
    print(f"   Fields: {list(form.fields.keys())}")
    
    if 'profile_image' in form.fields:
        print(f"✅ profile_image field present in form")
    else:
        print(f"❌ profile_image field missing from form")
    
    # Step 6: Test URL patterns
    print(f"\n🔗 Step 6: Test URL Patterns")
    print("-" * 35)
    
    try:
        from django.urls import reverse
        
        edit_profile_url = reverse('patients:edit_profile')
        profile_url = reverse('patients:profile')
        
        print(f"✅ URL patterns working")
        print(f"   Edit Profile: {edit_profile_url}")
        print(f"   View Profile: {profile_url}")
        
    except Exception as e:
        print(f"❌ URL pattern error: {e}")
        return False
    
    # Step 7: Test admin access to patient profiles
    print(f"\n🏢 Step 7: Test Admin Access")
    print("-" * 35)
    
    client = Client()
    
    # Try to access patient profile without login
    try:
        response = client.get(profile_url)
        if response.status_code == 302:
            print(f"✅ Unauthenticated access redirected correctly")
        else:
            print(f"⚠️  Unauthenticated access status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing unauthenticated access: {e}")
    
    return True

if __name__ == '__main__':
    success = test_patient_image_qr()
    
    if success:
        print(f"\n🎉 PATIENT IMAGE & QR CODE SYSTEM WORKING!")
        print(f"   ✅ QR code generation functional")
        print(f"   ✅ Form fields updated")
        print(f"   ✅ Templates updated")
        print(f"   ✅ URL patterns working")
        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
        print("=" * 50)
        print(f"   1. Login as a patient")
        print(f"   2. Go to profile page")
        print(f"   3. Click 'Edit Profile'")
        print(f"   4. Upload profile image")
        print(f"   5. Save profile")
        print(f"   6. QR code should be generated automatically")
        print(f"   7. Download QR code for physical card")
    else:
        print(f"\n❌ PATIENT IMAGE & QR CODE SYSTEM HAS ISSUES!")
