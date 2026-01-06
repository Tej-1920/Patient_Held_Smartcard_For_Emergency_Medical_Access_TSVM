#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from patients.models import Patient
from django.test import Client

def fix_emergency_display_final():
    """Final fix for emergency access display issues"""
    
    print("🚨 FIXING EMERGENCY ACCESS DISPLAY")
    print("=" * 45)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    # Use a very unique registration number that won't be in any list
    unique_registration = f"EMERGENCY{doctor.id}"
    print(f"Setting unique registration: {unique_registration}")
    
    # Update doctor
    doctor.nmc_registration_number = unique_registration
    doctor.save()
    print(f"✅ Doctor registration updated")
    
    print(f"\n📋 PATIENT DATA:")
    print("-" * 25)
    print(f"Emergency Contact Name: '{patient.emergency_contact_name}'")
    print(f"Emergency Contact Phone: '{patient.emergency_contact_phone}'")
    print(f"Emergency Contact Relation: '{patient.emergency_contact_relation}'")
    
    print(f"\n📁 MEDICAL RECORDS:")
    print("-" * 20)
    records = patient.medical_records.all()
    print(f"Total Records: {records.count()}")
    
    for i, record in enumerate(records, 1):
        print(f"Record {i}: {record.get_record_type_display()} - {record.title}")
        print(f"  File: {record.file.url if record.file else 'None'}")
    
    print(f"\n🚨 TESTING EMERGENCY ACCESS:")
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
            'registration_number': unique_registration,
            'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
            'access_reason': 'Emergency test - patient requires immediate medical attention'
        }, follow=True)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            print(f"\n📊 CHECKING DISPLAY:")
            print("-" * 25)
            
            # Check for emergency access granted
            if "Emergency Access Granted" in content:
                print(f"✅ Emergency Access Granted: Found")
            else:
                print(f"❌ Emergency Access Granted: NOT found")
                print(f"   Looking for alternative indicators...")
                
                # Check if patient information is displayed
                if patient.first_name in content:
                    print(f"✅ Patient Name: Found")
                else:
                    print(f"❌ Patient Name: NOT found")
                    
                if patient.patient_id in content:
                    print(f"✅ Patient ID: Found")
                else:
                    print(f"❌ Patient ID: NOT found")
            
            # Check emergency contact display
            print(f"\n📞 EMERGENCY CONTACT:")
            print("-" * 25)
            
            if patient.emergency_contact_name and patient.emergency_contact_name in content:
                print(f"✅ Emergency Contact Name: Found")
            else:
                print(f"❌ Emergency Contact Name: NOT found")
                
            if patient.emergency_contact_phone and patient.emergency_contact_phone in content:
                print(f"✅ Emergency Contact Phone: Found")
            else:
                print(f"❌ Emergency Contact Phone: NOT found")
                
            if patient.emergency_contact_relation and patient.emergency_contact_relation in content:
                print(f"✅ Emergency Contact Relation: Found")
            else:
                print(f"❌ Emergency Contact Relation: NOT found")
            
            # Check medical records display
            print(f"\n📁 MEDICAL RECORDS:")
            print("-" * 20)
            
            if "Medical Records" in content:
                print(f"✅ Medical Records Section: Found")
            else:
                print(f"❌ Medical Records Section: NOT found")
            
            for i, record in enumerate(records, 1):
                record_type_display = record.get_record_type_display()
                if record_type_display and record_type_display in content:
                    print(f"✅ Record {i} Type ({record_type_display}): Found")
                else:
                    print(f"❌ Record {i} Type ({record_type_display}): NOT found")
                    
                if record.file and record.file.url and record.file.url in content:
                    print(f"✅ Record {i} Download Link: Found")
                else:
                    print(f"❌ Record {i} Download Link: NOT found")
            
            # Show content snippet
            print(f"\n📄 CONTENT SNIPPET:")
            print("-" * 25)
            
            # Find emergency contact section
            if "Emergency Contact" in content:
                start = content.find("Emergency Contact")
                end = content.find("Medical Information", start)
                if end == -1:
                    end = start + 300
                snippet = content[start:end]
                print(snippet[:200])
            else:
                # Look for any patient data
                if patient.first_name in content:
                    start = content.find(patient.first_name) - 50
                    end = start + 300
                    snippet = content[start:end]
                    print(snippet[:200])
                else:
                    print("No patient data found in content")
            
        else:
            print(f"❌ Emergency access failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")
    
    print(f"\n🎯 MANUAL TESTING INSTRUCTIONS:")
    print("=" * 40)
    print(f"1. Restart Django server:")
    print(f"   python manage.py runserver")
    print(f"")
    print(f"2. Login as doctor:")
    print(f"   URL: http://127.0.0.1:8000/doctor/login/")
    print(f"   Email: chaitanyauggina@gmail.com")
    print(f"   Password: doctor123")
    print(f"")
    print(f"3. Access emergency page:")
    print(f"   URL: http://127.0.0.1:8000/doctor/emergency-access/")
    print(f"")
    print(f"4. Test emergency access:")
    print(f"   Patient ID: {patient.patient_id}")
    print(f"   Registration: {unique_registration}")
    print(f"   Council: Andhra Pradesh Medical Council")
    print(f"   Reason: Emergency test - patient requires immediate medical attention")
    print(f"")
    print(f"5. Expected results:")
    print(f"   ✅ Emergency access granted")
    print(f"   ✅ Emergency contact: {patient.emergency_contact_name} ({patient.emergency_contact_relation})")
    print(f"   ✅ Emergency phone: {patient.emergency_contact_phone}")
    print(f"   ✅ Medical records: {records.count()} files with download links")

if __name__ == '__main__':
    fix_emergency_display_final()
