#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def test_file_fix():
    """Test the file condition fix"""
    
    print("🔍 TESTING FILE CONDITION FIX")
    print("=" * 35)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
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
            
            print(f"\n📊 CHECKING FILE CONDITION FIX:")
            print("-" * 40)
            
            # Check for new condition
            if "record.file and record.file.name" in content:
                print(f"✅ New file condition found in template")
            else:
                print(f"❌ New file condition NOT found")
            
            # Check for enhanced error message
            if "NO FILE FOUND - CHECK RECORD ID:" in content:
                print(f"❌ Still showing 'NO FILE FOUND' message")
                error_count = content.count("NO FILE FOUND - CHECK RECORD ID:")
                print(f"   Error messages found: {error_count}")
            else:
                print(f"✅ No 'NO FILE FOUND' messages")
            
            # Check for download buttons
            if "Download File" in content:
                download_count = content.count("Download File")
                print(f"✅ Download buttons found: {download_count}")
            else:
                print(f"❌ Download buttons NOT found")
            
            # Check for file URLs
            records = patient.medical_records.all()
            file_url_count = 0
            for record in records:
                if record.file and record.file.url and record.file.url in content:
                    file_url_count += 1
            print(f"✅ File URLs found: {file_url_count}")
            
            # Show medical records section
            print(f"\n📄 MEDICAL RECORDS SECTION:")
            print("-" * 35)
            
            if "Medical Records" in content:
                start = content.find("Medical Records")
                end = content.find("Access Information", start)
                if end == -1:
                    end = start + 1000
                snippet = content[start:end]
                print(snippet[:800])
            else:
                print("Medical Records section not found")
            
            # Final assessment
            print(f"\n🎯 ASSESSMENT:")
            print("-" * 20)
            
            if "NO FILE FOUND - CHECK RECORD ID:" in content:
                print("❌ Still showing file not found messages")
                print("   This means the condition is still evaluating to False")
                print("   There might be a template caching issue")
            else:
                print("✅ File condition appears to be working")
            
            print(f"\n📝 NEXT STEPS:")
            print("-" * 20)
            print("1. Restart Django server to clear template cache")
            print("2. Clear browser cache (Ctrl+F5)")
            print("3. Check browser developer tools for actual HTML")
            print("4. Look for the new debug messages in page source")
        
        else:
            print(f"❌ Emergency access failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")

if __name__ == '__main__':
    test_file_fix()
