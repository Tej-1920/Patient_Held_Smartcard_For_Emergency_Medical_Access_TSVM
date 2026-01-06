#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

def fix_patient_login():
    """Fix patient login credentials"""
    
    print("🔐 FIXING PATIENT LOGIN")
    print("=" * 35)
    
    patients = Patient.objects.all()
    
    for patient in patients:
        # Set a known password for testing
        patient.set_password('patient123')
        patient.save()
        
        print(f"✅ {patient.first_name} {patient.last_name}")
        print(f"   Email: {patient.email}")
        print(f"   Password: patient123")
        print(f"   Patient ID: {patient.patient_id}")
        print()
    
    print("🎯 LOGIN INSTRUCTIONS:")
    print("=" * 30)
    print("1. Go to: http://127.0.0.1:8000/patient/login/")
    print("2. Use any patient email above")
    print("3. Password: patient123")
    print("4. Click login")
    print()
    print("👤 PATIENT WITH IMAGE:")
    print("tejaswiniuggina282@gmail.com")
    print("Password: patient123")
    print("✅ This patient has profile image!")

if __name__ == '__main__':
    fix_patient_login()
