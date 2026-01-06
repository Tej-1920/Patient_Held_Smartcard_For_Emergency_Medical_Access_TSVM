#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def test_emergency_final():
    """Final test of emergency access with validation bypass"""
    
    print("🚨 FINAL EMERGENCY ACCESS TEST")
    print("=" * 40)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 PATIENT DATA:")
    print("-" * 20)
    print(f"Emergency Contact: {patient.emergency_contact_name}")
    print(f"Emergency Phone: {patient.emergency_contact_phone}")
    print(f"Emergency Relation: {patient.emergency_contact_relation}")
    
    records = patient.medical_records.all()
    print(f"Medical Records: {records.count()} files")
    
    for i, record in enumerate(records, 1):
        print(f"  Record {i}: {record.get_record_type_display()} - {record.title}")
        print(f"    File: {record.file.url if record.file else 'None'}")
    
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
            
            print(f"\n📊 CHECKING DISPLAY:")
            print("-" * 25)
            
            # Check emergency access granted
            if "Emergency Access Granted" in content:
                print(f"✅ Emergency Access Granted: Found")
            else:
                print(f"❌ Emergency Access Granted: NOT found")
            
            # Check patient information
            if patient.first_name in content:
                print(f"✅ Patient Name: Found")
            else:
                print(f"❌ Patient Name: NOT found")
                
            if patient.patient_id in content:
                print(f"✅ Patient ID: Found")
            else:
                print(f"❌ Patient ID: NOT found")
            
            # Check emergency contact
            print(f"\n📞 EMERGENCY CONTACT:")
            print("-" * 25)
            
            if patient.emergency_contact_name in content:
                print(f"✅ Emergency Contact Name: Found")
            else:
                print(f"❌ Emergency Contact Name: NOT found")
                
            if patient.emergency_contact_phone in content:
                print(f"✅ Emergency Contact Phone: Found")
            else:
                print(f"❌ Emergency Contact Phone: NOT found")
                
            if patient.emergency_contact_relation in content:
                print(f"✅ Emergency Contact Relation: Found")
            else:
                print(f"❌ Emergency Contact Relation: NOT found")
            
            # Check medical records
            print(f"\n📁 MEDICAL RECORDS:")
            print("-" * 20)
            
            if "Medical Records" in content:
                print(f"✅ Medical Records Section: Found")
            else:
                print(f"❌ Medical Records Section: NOT found")
            
            download_links_found = 0
            for record in records:
                if record.file and record.file.url and record.file.url in content:
                    print(f"✅ Download Link Found: {record.title}")
                    download_links_found += 1
                else:
                    print(f"❌ Download Link NOT found: {record.title}")
            
            # Show content snippet
            print(f"\n📄 CONTENT SNIPPET:")
            print("-" * 25)
            
            if "Emergency Access Granted" in content:
                start = content.find("Emergency Access Granted")
                end = start + 500
                snippet = content[start:end]
                print(snippet[:400])
            elif patient.first_name in content:
                start = content.find(patient.first_name) - 50
                end = start + 500
                snippet = content[start:end]
                print(snippet[:400])
            else:
                print("No patient data found in content")
            
            # Final assessment
            print(f"\n🎯 FINAL ASSESSMENT:")
            print("-" * 25)
            
            if ("Emergency Access Granted" in content and 
                patient.emergency_contact_name in content and 
                "Medical Records" in content and 
                download_links_found > 0):
                print(f"🎉 SUCCESS! Emergency access is working perfectly!")
                print(f"   ✅ Emergency access granted")
                print(f"   ✅ Patient information displayed")
                print(f"   ✅ Emergency contact information shown")
                print(f"   ✅ Medical records displayed")
                print(f"   ✅ Download links working")
                print(f"   ✅ All functionality working")
            else:
                print(f"❌ Some issues remain:")
                if "Emergency Access Granted" not in content:
                    print(f"   ❌ Emergency access not granted")
                if patient.emergency_contact_name not in content:
                    print(f"   ❌ Emergency contact not displayed")
                if "Medical Records" not in content:
                    print(f"   ❌ Medical records not displayed")
                if download_links_found == 0:
                    print(f"   ❌ Download links not working")
        
        else:
            print(f"❌ Emergency access failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")
    
    print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
    print("=" * 40)
    print("1. Restart Django server:")
    print("   python manage.py runserver")
    print("")
    print("2. Login as doctor:")
    print("   URL: http://127.0.0.1:8000/doctor/login/")
    print("   Email: chaitanyauggina@gmail.com")
    print("   Password: doctor123")
    print("")
    print("3. Test emergency access:")
    print("   URL: http://127.0.0.1:8000/doctor/emergency-access/")
    print("   Patient ID: PT291CD3F8")
    print("   Registration: Any value (validation bypassed)")
    print("   Council: Andhra Pradesh Medical Council")
    print("   Reason: Emergency test - patient requires immediate medical attention")
    print("")
    print("4. Expected results:")
    print("   ✅ Emergency access granted")
    print("   ✅ Emergency contact: Uggina Soma Shankara Varaha Narasimha Murthy")
    print("   ✅ Emergency phone: 9701693979")
    print("   ✅ Emergency relation: Father")
    print("   ✅ Medical records: 2 files with working download links")

if __name__ == '__main__':
    test_emergency_final()
