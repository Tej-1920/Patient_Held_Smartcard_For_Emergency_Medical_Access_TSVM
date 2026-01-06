#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

def test_current_user_status():
    """Check which patients have images and provide login info"""
    
    print("🔍 PATIENT LOGIN STATUS & IMAGE INFO")
    print("=" * 50)
    
    patients = Patient.objects.all()
    
    print(f"\n👥 All Patients:")
    print("-" * 25)
    
    for i, patient in enumerate(patients, 1):
        print(f"\n{i}. {patient.first_name} {patient.last_name}")
        print(f"   Email: {patient.email}")
        print(f"   Patient ID: {patient.patient_id}")
        print(f"   Has Image: {'✅ Yes' if patient.profile_image else '❌ No'}")
        print(f"   Has QR: {'✅ Yes' if patient.qr_code else '❌ No'}")
        
        if patient.profile_image:
            print(f"   Image File: {patient.profile_image.name}")
            print(f"   Image URL: {patient.profile_image.url}")
    
    print(f"\n🔐 LOGIN INSTRUCTIONS:")
    print("-" * 30)
    
    # Find patient with image
    patient_with_image = Patient.objects.filter(profile_image__isnull=False).first()
    
    if patient_with_image:
        print(f"\n✅ PATIENT WITH IMAGE FOUND:")
        print(f"   Name: {patient_with_image.first_name} {patient_with_image.last_name}")
        print(f"   Email: {patient_with_image.email}")
        print(f"   Patient ID: {patient_with_image.patient_id}")
        print(f"   Image: {patient_with_image.profile_image.name}")
        
        print(f"\n📝 TO TEST IMAGE DISPLAY:")
        print(f"   1. Login with: {patient_with_image.email}")
        print(f"   2. Password: (your password)")
        print(f"   3. Go to dashboard")
        print(f"   4. You should see the profile image!")
        
    else:
        print(f"\n❌ NO PATIENTS WITH IMAGES FOUND")
        print(f"   Upload an image first to test")
    
    print(f"\n📋 PATIENTS WITHOUT IMAGES:")
    print("-" * 35)
    
    patients_without_image = Patient.objects.filter(profile_image__isnull=True)
    for patient in patients_without_image:
        print(f"   ❌ {patient.first_name} {patient.last_name} ({patient.email})")
        print(f"      -> Upload image to see it on dashboard")
    
    print(f"\n💡 TROUBLESHOOTING:")
    print("-" * 25)
    print(f"   1. Make sure you're logged in as the correct patient")
    print(f"   2. Check browser console for 404 errors")
    print(f"   3. Clear browser cache")
    print(f"   4. Check network tab for failed image loads")
    print(f"   5. Verify Django dev server is running")

if __name__ == '__main__':
    test_current_user_status()
