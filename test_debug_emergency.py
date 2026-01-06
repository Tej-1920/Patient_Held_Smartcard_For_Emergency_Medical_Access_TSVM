#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def test_debug_emergency():
    """Test emergency access with debug information"""
    
    print("🔍 TESTING EMERGENCY ACCESS WITH DEBUG INFO")
    print("=" * 50)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 PATIENT RECORDS:")
    print("-" * 25)
    
    records = patient.medical_records.all()
    print(f"Total Records: {records.count()}")
    
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
            
            print(f"\n📊 CHECKING DEBUG INFORMATION:")
            print("-" * 40)
            
            # Check for debug comments
            if "DEBUG: Total records =" in content:
                print(f"✅ Debug comment for total records found")
                # Extract the number
                import re
                match = re.search(r'DEBUG: Total records = (\d+)', content)
                if match:
                    total_records = int(match.group(1))
                    print(f"   Total records reported: {total_records}")
            else:
                print(f"❌ Debug comment for total records NOT found")
            
            if "DEBUG: Records exist, showing" in content:
                print(f"✅ Debug comment for records exist found")
            else:
                print(f"❌ Debug comment for records exist NOT found")
            
            if "DEBUG: File exists -" in content:
                print(f"✅ Debug comment for file exists found")
                file_debug_count = content.count("DEBUG: File exists -")
                print(f"   File debug comments found: {file_debug_count}")
            else:
                print(f"❌ Debug comment for file exists NOT found")
            
            if "DEBUG: No file found" in content:
                print(f"❌ Debug comment for no file found (should not appear)")
            else:
                print(f"✅ No 'no file' debug comments (good)")
            
            # Check for enhanced download buttons
            if "Download File" in content:
                download_count = content.count("Download File")
                print(f"✅ Enhanced download buttons found: {download_count}")
            else:
                print(f"❌ Enhanced download buttons NOT found")
            
            # Check for blue background styling
            if "background-color: #007bff !important" in content:
                print(f"✅ Blue background styling found")
            else:
                print(f"❌ Blue background styling NOT found")
            
            # Show medical records section with debug info
            print(f"\n📄 MEDICAL RECORDS SECTION WITH DEBUG:")
            print("-" * 50)
            
            if "Medical Records" in content:
                start = content.find("Medical Records")
                end = content.find("Access Information", start)
                if end == -1:
                    end = start + 1200
                snippet = content[start:end]
                print(snippet[:1000])
            else:
                print("Medical Records section not found")
            
            print(f"\n🎯 INSTRUCTIONS FOR BROWSER TESTING:")
            print("-" * 45)
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
            print("4. In browser, check:")
            print("   - View page source (Ctrl+U)")
            print("   - Look for DEBUG comments")
            print("   - Check for 'Download File' buttons")
            print("   - Look for blue download buttons")
            print("   - Right-click and 'Inspect Element' on download area")
            print("")
            print("5. If still not visible:")
            print("   - Clear browser cache (Ctrl+F5)")
            print("   - Try different browser")
            print("   - Check browser console for errors")
        
        else:
            print(f"❌ Emergency access failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")

if __name__ == '__main__':
    test_debug_emergency()
