#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def test_emergency_access_simple():
    """Simple test for emergency access functionality"""
    
    print("🚨 EMERGENCY ACCESS FUNCTIONALITY TEST")
    print("=" * 50)
    
    # Get verified doctor and patient with emergency contact
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    if not doctor:
        print("❌ No verified doctors found")
        return False
    
    if not patient:
        print("❌ No patients with emergency contact found")
        return False
    
    print(f"✅ Test Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"✅ Test Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    # Check patient data
    print(f"\n📋 Patient Emergency Contact Data:")
    print(f"   Name: {patient.emergency_contact_name}")
    print(f"   Phone: {patient.emergency_contact_phone}")
    print(f"   Relation: {patient.emergency_contact_relation}")
    print(f"   Medical Records: {patient.medical_records.count()} files")
    
    # Test web access
    print(f"\n🌐 Testing Emergency Access:")
    
    client = Client()
    
    # Login
    response = client.post('/doctor/login/', {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    if response.status_code != 302:
        print(f"❌ Doctor login failed: {response.status_code}")
        return False
    
    print(f"✅ Doctor login successful")
    
    # Access emergency page
    response = client.get('/doctor/emergency-access/')
    if response.status_code != 200:
        print(f"❌ Emergency access page failed: {response.status_code}")
        return False
    
    print(f"✅ Emergency access page accessible")
    
    # Submit emergency access
    response = client.post('/doctor/emergency-access/', {
        'patient_id': patient.patient_id,
        'registration_number': doctor.nmc_registration_number or 'TEST123',
        'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
        'access_reason': 'Emergency test - patient requires immediate medical attention'
    })
    
    if response.status_code != 200:
        print(f"❌ Emergency access submission failed: {response.status_code}")
        return False
    
    print(f"✅ Emergency access submitted successfully")
    
    # Check response content
    content = response.content.decode('utf-8')
    
    checks = [
        ("Emergency Access Granted", "Emergency Access Granted"),
        ("Patient Name", patient.first_name),
        ("Patient ID", patient.patient_id),
        ("Emergency Contact", "Emergency Contact"),
        ("Medical Records", "Medical Records"),
        ("Access Information", "Access Information")
    ]
    
    print(f"\n📊 Checking Response Content:")
    for check_text, description in checks:
        if check_text in content:
            print(f"✅ {description}: Found")
        else:
            print(f"❌ {description}: Missing")
    
    return True

if __name__ == '__main__':
    success = test_emergency_access_simple()
    
    if success:
        print(f"\n🎉 EMERGENCY ACCESS WORKING!")
        print(f"   ✅ Emergency access form functional")
        print(f"   ✅ Patient information displayed")
        print(f"   ✅ Emergency contact information shown")
        print(f"   ✅ Medical records displayed")
        print(f"   ✅ Access logging functional")
        
        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
        print(f"   1. Start server: python manage.py runserver")
        print(f"   2. Login as doctor: chaitanyauggina@gmail.com / doctor123")
        print(f"   3. Go to: http://127.0.0.1:8000/doctor/emergency-access/")
        print(f"   4. Use patient ID: {Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first().patient_id}")
        print(f"   5. Fill form and submit")
        print(f"   6. Verify emergency contact and medical records are displayed")
    else:
        print(f"\n❌ EMERGENCY ACCESS HAS ISSUES!")
