#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

def check_patient_data():
    """Check which patients have complete data"""
    
    print("👤 CHECKING PATIENT DATA")
    print("=" * 30)
    
    patients = Patient.objects.all()
    
    for patient in patients:
        print(f"\n📋 Patient: {patient.first_name} {patient.last_name}")
        print(f"   ID: {patient.patient_id}")
        print(f"   Email: {patient.email}")
        print(f"   Phone: {patient.phone_number}")
        print(f"   Profile Image: {'✅' if patient.profile_image else '❌'}")
        print(f"   QR Code: {'✅' if patient.qr_code else '❌'}")
        print(f"   Emergency Contact Name: {'✅' if patient.emergency_contact_name else '❌'}")
        print(f"   Emergency Contact Phone: {'✅' if patient.emergency_contact_phone else '❌'}")
        print(f"   Emergency Contact Relation: {'✅' if patient.emergency_contact_relation else '❌'}")
        print(f"   Chronic Diseases: {'✅' if patient.chronic_diseases else '❌'}")
        print(f"   Allergies: {'✅' if patient.allergies else '❌'}")
        print(f"   Medical Records: {patient.medical_records.count()} files")
        
        # Check if this patient has emergency contact data
        if patient.emergency_contact_name:
            print(f"   🚨 THIS PATIENT HAS EMERGENCY CONTACT DATA!")
            print(f"   🎯 Use this ID for emergency access testing: {patient.patient_id}")

if __name__ == '__main__':
    check_patient_data()
