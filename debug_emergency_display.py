#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from patients.models import Patient

def debug_emergency_display():
    """Debug emergency access display issues"""
    
    print("🔍 DEBUGGING EMERGENCY ACCESS DISPLAY")
    print("=" * 50)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 PATIENT EMERGENCY CONTACT DATA:")
    print("-" * 40)
    print(f"Emergency Contact Name: '{patient.emergency_contact_name}'")
    print(f"Emergency Contact Phone: '{patient.emergency_contact_phone}'")
    print(f"Emergency Contact Relation: '{patient.emergency_contact_relation}'")
    
    print(f"\n📁 PATIENT MEDICAL RECORDS:")
    print("-" * 35)
    records = patient.medical_records.all()
    print(f"Total Records: {records.count()}")
    
    for i, record in enumerate(records, 1):
        print(f"\nRecord {i}:")
        print(f"  ID: {record.id}")
        print(f"  Record Type: '{record.record_type}'")
        print(f"  Title: '{record.title}'")
        print(f"  Description: '{record.description}'")
        print(f"  File: '{record.file}'")
        print(f"  File URL: '{record.file.url if record.file else 'None'}")
        print(f"  Uploaded At: {record.uploaded_at}")
        print(f"  File Exists: {record.file and os.path.exists(record.file.path) if record.file else False}")
    
    print(f"\n🌐 TESTING TEMPLATE RENDERING:")
    print("-" * 40)
    
    from django.test import Client
    from django.template.loader import render_to_string
    
    # Login and get emergency access response
    client = Client()
    
    # Login
    response = client.post('/doctor/login/', {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    if response.status_code == 302:
        print("✅ Doctor login successful")
        
        # Submit emergency access
        response = client.post('/doctor/emergency-access/', {
            'patient_id': patient.patient_id,
            'registration_number': doctor.nmc_registration_number,
            'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
            'access_reason': 'Emergency test - patient requires immediate medical attention'
        }, follow=True)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            print(f"\n📊 CHECKING EMERGENCY CONTACT DISPLAY:")
            print("-" * 50)
            
            # Check emergency contact display
            if patient.emergency_contact_name and patient.emergency_contact_name in content:
                print(f"✅ Emergency Contact Name: Found in content")
            else:
                print(f"❌ Emergency Contact Name: NOT found in content")
                
            if patient.emergency_contact_phone and patient.emergency_contact_phone in content:
                print(f"✅ Emergency Contact Phone: Found in content")
            else:
                print(f"❌ Emergency Contact Phone: NOT found in content")
                
            if patient.emergency_contact_relation and patient.emergency_contact_relation in content:
                print(f"✅ Emergency Contact Relation: Found in content")
            else:
                print(f"❌ Emergency Contact Relation: NOT found in content")
            
            print(f"\n📊 CHECKING MEDICAL RECORDS DISPLAY:")
            print("-" * 45)
            
            # Check medical records display
            if "Medical Records" in content:
                print(f"✅ Medical Records Section: Found")
            else:
                print(f"❌ Medical Records Section: NOT found")
            
            for i, record in enumerate(records, 1):
                if record.record_type and record.get_record_type_display() in content:
                    print(f"✅ Record {i} Type: Found")
                else:
                    print(f"❌ Record {i} Type: NOT found")
                    
                if record.file and record.file.url and record.file.url in content:
                    print(f"✅ Record {i} Download Link: Found")
                else:
                    print(f"❌ Record {i} Download Link: NOT found")
            
            # Check for specific template elements
            print(f"\n📊 CHECKING TEMPLATE ELEMENTS:")
            print("-" * 40)
            
            elements = [
                ("Emergency Contact", "Emergency Contact"),
                ("Medical Records", "Medical Records"),
                ("Download button", "Download"),
                ("Document type display", "document_type"),
                ("File link", ".pdf" or ".jpg" or ".png")
            ]
            
            for element_name, search_text in elements:
                if search_text in content:
                    print(f"✅ {element_name}: Found")
                else:
                    print(f"❌ {element_name}: NOT found")
            
            # Show relevant content snippet
            print(f"\n📄 CONTENT SNIPPET:")
            print("-" * 25)
            
            # Find and show emergency contact section
            if "Emergency Contact" in content:
                start = content.find("Emergency Contact")
                end = content.find("Medical Information", start)
                if end == -1:
                    end = start + 500
                snippet = content[start:end]
                print(snippet[:300])
            
        else:
            print(f"❌ Emergency access failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")

if __name__ == '__main__':
    debug_emergency_display()
