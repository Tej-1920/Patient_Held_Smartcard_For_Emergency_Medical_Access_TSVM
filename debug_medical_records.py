#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient
from django.conf import settings

def debug_medical_records():
    """Debug medical records file serving issues"""
    
    print("🔍 DEBUGGING MEDICAL RECORDS FILE SERVING")
    print("=" * 50)
    
    # Get patient with medical records
    patient = Patient.objects.filter(medical_records__isnull=False).first()
    
    if not patient:
        print("❌ No patient with medical records found")
        return
    
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📁 MEDIA SETTINGS:")
    print("-" * 25)
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"DEBUG: {settings.DEBUG}")
    
    print(f"\n📋 MEDICAL RECORDS:")
    print("-" * 25)
    
    records = patient.medical_records.all()
    print(f"Total Records: {records.count()}")
    
    for i, record in enumerate(records, 1):
        print(f"\nRecord {i}:")
        print(f"  ID: {record.id}")
        print(f"  Title: {record.title}")
        print(f"  Type: {record.get_record_type_display()}")
        print(f"  Description: {record.description}")
        print(f"  File Field: {record.file}")
        print(f"  File URL: {record.file.url if record.file else 'None'}")
        print(f"  File Path: {record.file.path if record.file else 'None'}")
        
        if record.file:
            # Check if file exists on disk
            file_exists = os.path.exists(record.file.path)
            print(f"  File Exists: {file_exists}")
            
            if file_exists:
                # Check file size
                try:
                    file_size = os.path.getsize(record.file.path)
                    print(f"  File Size: {file_size} bytes")
                except Exception as e:
                    print(f"  File Size Error: {e}")
                
                # Check file extension
                file_ext = os.path.splitext(record.file.path)[1].lower()
                print(f"  File Extension: {file_ext}")
            else:
                print(f"  ❌ FILE NOT FOUND ON DISK")
        
        print(f"  Uploaded At: {record.uploaded_at}")
    
    print(f"\n🌐 TESTING FILE URLS:")
    print("-" * 30)
    
    from django.test import Client
    
    client = Client()
    
    for i, record in enumerate(records, 1):
        if record.file:
            file_url = record.file.url
            print(f"\nRecord {i} - {record.title}:")
            print(f"  URL: {file_url}")
            
            # Test if URL is accessible
            try:
                response = client.get(file_url)
                print(f"  Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  ✅ File accessible via URL")
                    print(f"  Content-Type: {response.get('Content-Type', 'Unknown')}")
                    print(f"  Content-Length: {response.get('Content-Length', 'Unknown')}")
                elif response.status_code == 404:
                    print(f"  ❌ File not found (404)")
                elif response.status_code == 302:
                    print(f"  ⚠️  Redirect (302) - might be login required")
                else:
                    print(f"  ❌ Unexpected status: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Error accessing URL: {e}")
    
    print(f"\n🔧 POSSIBLE ISSUES:")
    print("-" * 25)
    
    issues = []
    
    # Check media directory
    if not os.path.exists(settings.MEDIA_ROOT):
        issues.append("MEDIA_ROOT directory does not exist")
    
    # Check medical records directory
    medical_records_dir = os.path.join(settings.MEDIA_ROOT, 'medical_records')
    if not os.path.exists(medical_records_dir):
        issues.append("medical_records directory does not exist")
    
    # Check if files exist
    for record in records:
        if record.file and not os.path.exists(record.file.path):
            issues.append(f"File not found: {record.file.path}")
    
    # Check URL configuration
    if settings.DEBUG:
        print("✅ DEBUG mode - Django should serve media files")
    else:
        issues.append("DEBUG mode is False - need to configure media file serving")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ No obvious configuration issues found")
    
    print(f"\n📝 SOLUTIONS:")
    print("-" * 20)
    
    print("1. Check if files exist in the correct location")
    print("2. Ensure MEDIA_URL and MEDIA_ROOT are configured correctly")
    print("3. Verify URL patterns include media file serving")
    print("4. Check file permissions")
    print("5. Test file URLs directly in browser")
    
    print(f"\n🎯 MANUAL TESTING:")
    print("-" * 25)
    print("1. Start server: python manage.py runserver")
    print("2. Login as doctor and access emergency page")
    print("3. Try clicking download links")
    print("4. Check browser network tab for URL requests")
    print("5. Verify file URLs are accessible directly")

if __name__ == '__main__':
    debug_medical_records()
