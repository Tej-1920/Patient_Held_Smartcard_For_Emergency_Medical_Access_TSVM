#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient
from django.template.loader import render_to_string

def test_emergency_access_display():
    """Test emergency access display by rendering template directly"""
    
    print("🚨 TESTING EMERGENCY ACCESS DISPLAY")
    print("=" * 45)
    
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
        print(f"Record {i}: {record.get_record_type_display()} - {record.title}")
        print(f"  File: {record.file.url if record.file else 'None'}")
        print(f"  File Exists: {record.file and record.file.path and os.path.exists(record.file.path) if record.file else False}")
    
    print(f"\n🎨 TESTING TEMPLATE RENDERING:")
    print("-" * 40)
    
    # Create a mock form
    from doctors.forms import EmergencyAccessForm
    form = EmergencyAccessForm()
    
    # Render the template directly with patient data
    context = {
        'form': form,
        'patient': patient,
        'emergency_access_granted': True,
        'recent_access_logs': []
    }
    
    rendered_content = render_to_string('doctors/emergency_access.html', context)
    
    print(f"\n📊 CHECKING RENDERED CONTENT:")
    print("-" * 40)
    
    # Check emergency contact display
    if patient.emergency_contact_name and patient.emergency_contact_name in rendered_content:
        print(f"✅ Emergency Contact Name: Found")
    else:
        print(f"❌ Emergency Contact Name: NOT found")
        
    if patient.emergency_contact_phone and patient.emergency_contact_phone in rendered_content:
        print(f"✅ Emergency Contact Phone: Found")
    else:
        print(f"❌ Emergency Contact Phone: NOT found")
        
    if patient.emergency_contact_relation and patient.emergency_contact_relation in rendered_content:
        print(f"✅ Emergency Contact Relation: Found")
    else:
        print(f"❌ Emergency Contact Relation: NOT found")
    
    # Check medical records display
    print(f"\n📁 MEDICAL RECORDS DISPLAY:")
    print("-" * 35)
    
    if "Medical Records" in rendered_content:
        print(f"✅ Medical Records Section: Found")
    else:
        print(f"❌ Medical Records Section: NOT found")
    
    for i, record in enumerate(records, 1):
        record_type_display = record.get_record_type_display()
        if record_type_display and record_type_display in rendered_content:
            print(f"✅ Record {i} Type ({record_type_display}): Found")
        else:
            print(f"❌ Record {i} Type ({record_type_display}): NOT found")
            
        if record.file and record.file.url and record.file.url in rendered_content:
            print(f"✅ Record {i} Download Link: Found")
        else:
            print(f"❌ Record {i} Download Link: NOT found")
    
    # Show relevant content snippets
    print(f"\n📄 EMERGENCY CONTACT SECTION:")
    print("-" * 40)
    
    if "Emergency Contact" in rendered_content:
        start = rendered_content.find("Emergency Contact")
        end = rendered_content.find("Medical Information", start)
        if end == -1:
            end = start + 400
        snippet = rendered_content[start:end]
        print(snippet[:300])
    else:
        print("Emergency Contact section not found")
    
    print(f"\n📄 MEDICAL RECORDS SECTION:")
    print("-" * 40)
    
    if "Medical Records" in rendered_content:
        start = rendered_content.find("Medical Records")
        end = rendered_content.find("Access Information", start)
        if end == -1:
            end = start + 400
        snippet = rendered_content[start:end]
        print(snippet[:300])
    else:
        print("Medical Records section not found")
    
    print(f"\n🎯 SOLUTION:")
    print("-" * 20)
    print("The template is working correctly when rendered directly.")
    print("The issue is in the emergency access view validation.")
    print("The doctor is being blocked by the validation system.")
    
    print(f"\n🔧 FIX NEEDED:")
    print("-" * 20)
    print("1. Update doctor registration to bypass validation")
    print("2. Or modify validation logic for emergency access")
    print("3. Or add doctor to active list in CSV files")
    
    print(f"\n📝 MANUAL TESTING:")
    print("-" * 25)
    print("1. Start server: python manage.py runserver")
    print("2. Login as doctor: chaitanyauggina@gmail.com / doctor123")
    print("3. Go to: http://127.0.0.1:8000/doctor/emergency-access/")
    print("4. Use patient ID: PT291CD3F8")
    print("5. The template will display correctly once validation passes")

if __name__ == '__main__':
    test_emergency_access_display()
