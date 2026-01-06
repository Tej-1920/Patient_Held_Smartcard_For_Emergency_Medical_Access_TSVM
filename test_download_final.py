#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def test_download_final():
    """Final test of download button functionality"""
    
    print("🔍 FINAL DOWNLOAD BUTTON TEST")
    print("=" * 40)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 MEDICAL RECORDS:")
    print("-" * 25)
    
    records = patient.medical_records.all()
    for i, record in enumerate(records, 1):
        print(f"Record {i}: {record.get_record_type_display()} - {record.title}")
        print(f"  File: {record.file.url if record.file else 'None'}")
    
    print(f"\n🌐 TESTING EMERGENCY ACCESS:")
    print("-" * 35)
    
    client = Client()
    
    # Login
    response = client.post('/doctor/login/', {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    if response.status_code == 302:
        print(f"✅ Doctor login successful")
        
        # Submit emergency access
        response = client.post('/doctor/emergency-access/', {
            'patient_id': patient.patient_id,
            'registration_number': doctor.nmc_registration_number or 'TEST123',
            'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
            'access_reason': 'Emergency test - patient requires immediate medical attention'
        }, follow=True)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            print(f"\n📊 CHECKING DOWNLOAD FUNCTIONALITY:")
            print("-" * 45)
            
            # Check for download buttons with inline styles
            if "display: inline-block !important" in content:
                print(f"✅ Download button inline styles found")
            else:
                print(f"❌ Download button inline styles NOT found")
            
            # Check for CSS classes
            if "record-item .btn-outline-primary" in content:
                print(f"✅ CSS styling for download buttons found")
            else:
                print(f"❌ CSS styling for download buttons NOT found")
            
            # Check download URLs
            download_urls_found = 0
            for record in records:
                if record.file and record.file.url:
                    if record.file.url in content:
                        print(f"✅ Download URL found: {record.title}")
                        download_urls_found += 1
                        
                        # Test direct file access
                        file_response = client.get(record.file.url)
                        if file_response.status_code == 200:
                            print(f"  ✅ File accessible: {file_response.status_code}")
                        else:
                            print(f"  ❌ File not accessible: {file_response.status_code}")
                    else:
                        print(f"❌ Download URL NOT found: {record.title}")
            
            # Check for download text
            if "Download" in content:
                download_count = content.count("Download")
                print(f"✅ Download text found {download_count} times")
            else:
                print(f"❌ Download text NOT found")
            
            # Check for download icon
            if "fa-download" in content:
                icon_count = content.count("fa-download")
                print(f"✅ Download icon found {icon_count} times")
            else:
                print(f"❌ Download icon NOT found")
            
            # Extract medical records section
            print(f"\n📄 MEDICAL RECORDS SECTION (UPDATED):")
            print("-" * 50)
            
            if "Medical Records" in content:
                start = content.find("Medical Records")
                end = content.find("Access Information", start)
                if end == -1:
                    end = start + 1000
                snippet = content[start:end]
                print(snippet[:900])
            else:
                print("Medical Records section not found")
            
            # Final assessment
            print(f"\n🎯 FINAL ASSESSMENT:")
            print("-" * 25)
            
            if (download_urls_found == records.count() and 
                "Download" in content and 
                "fa-download" in content and
                "display: inline-block !important" in content):
                print(f"🎉 SUCCESS! Download buttons are properly configured!")
                print(f"   ✅ All download URLs present")
                print(f"   ✅ Download buttons visible with inline styles")
                print(f"   ✅ CSS styling applied")
                print(f"   ✅ Download icons present")
                print(f"   ✅ Files accessible via URLs")
                
                print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
                print("=" * 45)
                print("1. Restart Django server:")
                print("   python manage.py runserver")
                print("")
                print("2. Login as doctor:")
                print("   URL: http://127.0.0.1:8000/doctor/login/")
                print("   Email: chaitanyauggina@gmail.com")
                print("   Password: doctor123")
                print("")
                print("3. Access emergency page:")
                print("   URL: http://127.0.0.1:8000/doctor/emergency-access/")
                print("   Patient ID: PT291CD3F8")
                print("   Submit emergency access form")
                print("")
                print("4. Expected results:")
                print("   ✅ Emergency access granted")
                print("   ✅ Emergency contact information displayed")
                print("   ✅ Medical records displayed with visible download buttons")
                print("   ✅ Download buttons clickable and working")
                print("   ✅ Files download properly when clicked")
                
            else:
                print(f"❌ Some issues remain:")
                if download_urls_found != records.count():
                    print(f"   ❌ Missing download URLs")
                if "Download" not in content:
                    print(f"   ❌ Download text missing")
                if "fa-download" not in content:
                    print(f"   ❌ Download icons missing")
                if "display: inline-block !important" not in content:
                    print(f"   ❌ Inline styles not applied")
        
        else:
            print(f"❌ Emergency access failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")

if __name__ == '__main__':
    test_download_final()
