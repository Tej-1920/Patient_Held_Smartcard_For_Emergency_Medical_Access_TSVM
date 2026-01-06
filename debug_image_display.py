#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient
from django.conf import settings

def debug_image_display():
    """Debug patient image display issues"""
    
    print("🔍 DEBUGGING PATIENT IMAGE DISPLAY")
    print("=" * 50)
    
    # Step 1: Check Django settings
    print(f"\n⚙️  Step 1: Django Settings")
    print("-" * 35)
    
    print(f"Media URL: {settings.MEDIA_URL}")
    print(f"Media Root: {settings.MEDIA_ROOT}")
    
    # Check if media directory exists
    if os.path.exists(settings.MEDIA_ROOT):
        print(f"✅ Media directory exists")
        print(f"   Path: {settings.MEDIA_ROOT}")
        
        # Check subdirectories
        patient_images_dir = os.path.join(settings.MEDIA_ROOT, 'patient_images')
        qr_codes_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        
        print(f"\n📁 Directory Structure:")
        print(f"   patient_images/: {'✅ Exists' if os.path.exists(patient_images_dir) else '❌ Missing'}")
        print(f"   qr_codes/: {'✅ Exists' if os.path.exists(qr_codes_dir) else '❌ Missing'}")
        
        if os.path.exists(patient_images_dir):
            files = os.listdir(patient_images_dir)
            print(f"   Files in patient_images/: {len(files)} files")
            for file in files[:5]:  # Show first 5 files
                print(f"     - {file}")
        
    else:
        print(f"❌ Media directory does not exist")
        print(f"   Expected: {settings.MEDIA_ROOT}")
    
    # Step 2: Check patient data
    print(f"\n👤 Step 2: Patient Data Analysis")
    print("-" * 40)
    
    patients = Patient.objects.all()
    print(f"Total Patients: {patients.count()}")
    
    for i, patient in enumerate(patients, 1):
        print(f"\n   Patient {i}: {patient.first_name} {patient.last_name}")
        print(f"   ID: {patient.patient_id}")
        print(f"   Email: {patient.email}")
        
        # Check profile_image field
        if patient.profile_image:
            print(f"   ✅ Has profile_image: {patient.profile_image}")
            print(f"   ✅ Image name: {patient.profile_image.name}")
            print(f"   ✅ Image URL: {patient.profile_image.url}")
            print(f"   ✅ Image path: {patient.profile_image.path}")
            
            # Check if file actually exists
            if os.path.exists(patient.profile_image.path):
                print(f"   ✅ File exists on disk")
                
                # Check file size
                file_size = os.path.getsize(patient.profile_image.path)
                print(f"   ✅ File size: {file_size} bytes")
            else:
                print(f"   ❌ File NOT found on disk")
                print(f"   ❌ Expected path: {patient.profile_image.path}")
        else:
            print(f"   ❌ No profile_image")
        
        # Check qr_code field
        if patient.qr_code:
            print(f"   ✅ Has qr_code: {patient.qr_code.name}")
        else:
            print(f"   ❌ No qr_code")
    
    # Step 3: Test URL serving
    print(f"\n🌐 Step 3: URL Serving Test")
    print("-" * 35)
    
    # Check if media URLs are configured correctly
    from django.urls import reverse
    try:
        # Test media URL pattern
        print(f"Testing media URL configuration...")
        
        # Check if we can construct proper URLs
        test_patient = patients.first()
        if test_patient and test_patient.profile_image:
            print(f"✅ Image URL construction works")
            print(f"   URL: {test_patient.profile_image.url}")
        else:
            print(f"❌ No patient with image to test")
            
    except Exception as e:
        print(f"❌ URL construction error: {e}")
    
    # Step 4: Check Django project URLs
    print(f"\n🔗 Step 4: URL Configuration")
    print("-" * 35)
    
    # Check main urls.py
    main_urls_file = os.path.join(settings.BASE_DIR, 'patient_smart_card', 'urls.py')
    if os.path.exists(main_urls_file):
        print(f"✅ Main urls.py exists")
        
        with open(main_urls_file, 'r') as f:
            content = f.read()
            if 'static' in content and 'media' in content:
                print(f"✅ Static and media URLs configured")
            else:
                print(f"❌ Static/media URLs may be missing")
                print(f"Content preview:")
                print(content[:500])
    else:
        print(f"❌ Main urls.py not found")
    
    # Step 5: Recommendations
    print(f"\n💡 Step 5: Recommendations")
    print("-" * 35)
    
    has_issues = False
    
    for patient in patients:
        if patient.profile_image and not os.path.exists(patient.profile_image.path):
            has_issues = True
            print(f"❌ {patient.first_name}: Image file missing")
            print(f"   Fix: Re-upload image or check file permissions")
    
    if not os.path.exists(settings.MEDIA_ROOT):
        has_issues = True
        print(f"❌ Media directory missing")
        print(f"   Fix: Create media directory and configure permissions")
    
    if not has_issues:
        print(f"✅ No obvious issues found")
        print(f"   Check: Django development server running?")
        print(f"   Check: Browser cache cleared?")
        print(f"   Check: Network tab for 404 errors?")

if __name__ == '__main__':
    debug_image_display()
