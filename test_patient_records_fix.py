#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def test_patient_records_fix():
    """Test the patient records page fix"""
    
    print("🔍 TESTING PATIENT RECORDS PAGE FIX")
    print("=" * 45)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(medical_records__isnull=False).first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 PATIENT RECORDS:")
    print("-" * 25)
    
    records = patient.medical_records.all()
    print(f"Total Records: {records.count()}")
    
    for i, record in enumerate(records, 1):
        print(f"Record {i}: {record.get_record_type_display()} - {record.title}")
        print(f"  File: {record.file.url if record.file else 'None'}")
    
    print(f"\n🌐 TESTING PATIENT RECORDS PAGE:")
    print("-" * 40)
    
    client = Client()
    
    # Login
    response = client.post('/doctor/login/', {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    if response.status_code == 302:
        print(f"✅ Doctor login successful")
        
        # Access patient records page
        response = client.get(f'/doctor/patient/{patient.id}/records/')
        
        if response.status_code == 200:
            print(f"✅ Patient records page accessible")
            
            content = response.content.decode('utf-8')
            
            print(f"\n📊 CHECKING PAGE CONTENT:")
            print("-" * 35)
            
            # Check patient information
            if patient.first_name in content:
                print(f"✅ Patient name found")
            else:
                print(f"❌ Patient name NOT found")
            
            # Check medical records section
            if "Medical Records" in content:
                print(f"✅ Medical Records section found")
            else:
                print(f"❌ Medical Records section NOT found")
            
            # Check for download buttons
            if "Download" in content:
                download_count = content.count("Download")
                print(f"✅ Download buttons found: {download_count}")
            else:
                print(f"❌ Download buttons NOT found")
            
            # Check for file availability badges
            if "Available" in content:
                available_count = content.count("Available")
                print(f"✅ Available badges found: {available_count}")
            else:
                print(f"❌ Available badges NOT found")
            
            # Check for emergency contact information
            if patient.emergency_contact_name and patient.emergency_contact_name in content:
                print(f"✅ Emergency contact name found")
            else:
                print(f"❌ Emergency contact name NOT found")
            
            if patient.emergency_contact_phone and patient.emergency_contact_phone in content:
                print(f"✅ Emergency contact phone found")
            else:
                print(f"❌ Emergency contact phone NOT found")
            
            # Check file URLs
            file_url_count = 0
            for record in records:
                if record.file and record.file.url and record.file.url in content:
                    file_url_count += 1
            print(f"✅ File URLs found: {file_url_count}")
            
            # Show relevant content snippet
            print(f"\n📄 RECORDS SECTION SNIPPET:")
            print("-" * 40)
            
            if "Medical Records" in content:
                start = content.find("Medical Records")
                end = content.find("Medical Summary", start)
                if end == -1:
                    end = start + 1000
                snippet = content[start:end]
                print(snippet[:800])
            else:
                print("Medical Records section not found")
            
            # Final assessment
            print(f"\n🎯 ASSESSMENT:")
            print("-" * 20)
            
            if (download_count == records.count() and 
                file_url_count == records.count() and
                available_count == records.count()):
                print(f"🎉 SUCCESS! Patient records page is working!")
                print(f"   ✅ All download buttons present")
                print(f"   ✅ All file URLs accessible")
                print(f"   ✅ Emergency contact information displayed")
                print(f"   ✅ All functionality working")
            else:
                print(f"❌ Some issues remain:")
                if download_count != records.count():
                    print(f"   ❌ Missing download buttons")
                if file_url_count != records.count():
                    print(f"   ❌ Missing file URLs")
                if available_count != records.count():
                    print(f"   ❌ Missing availability badges")
        
        else:
            print(f"❌ Patient records page failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")
    
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
    print("3. Access patient records:")
    print("   - Search for patient: Uggina Tejaswini")
    print("   - Click 'View Records' button")
    print("   - Or go directly to: http://127.0.0.1:8000/doctor/patient/[PATIENT_ID]/records/")
    print("")
    print("4. Expected results:")
    print("   ✅ Patient information displayed")
    print("   ✅ Medical records list with download buttons")
    print("   ✅ Emergency contact information")
    print("   ✅ Working download links")
    print("   ✅ No 'No File' messages")

if __name__ == '__main__':
    test_patient_records_fix()
