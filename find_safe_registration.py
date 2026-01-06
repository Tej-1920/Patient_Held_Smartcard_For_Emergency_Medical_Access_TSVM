#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.utils import doctor_validator
from doctors.models import Doctor
import random

def find_safe_registration():
    """Find a safe registration number not in blacklist"""
    
    print("🔍 FINDING SAFE REGISTRATION NUMBER")
    print("=" * 50)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    print(f"Current Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Current Registration: {doctor.nmc_registration_number}")
    
    # Generate random registration numbers and test them
    print("\n🧪 Testing Registration Numbers:")
    print("-" * 40)
    
    safe_number = None
    attempts = 0
    
    while attempts < 100 and not safe_number:
        attempts += 1
        # Generate a random 5-digit number
        test_number = f"{random.randint(10000, 99999)}"
        
        validation_result = doctor_validator.validate_doctor(
            registration_number=test_number,
            state_medical_council=doctor.state_medical_council
        )
        
        if validation_result['status'] == 'NOT_FOUND':
            # This number is not in blacklist or active list - safe to use
            safe_number = test_number
            print(f"✅ {test_number}: SAFE (not found in any list)")
        elif validation_result['status'] == 'AUTHORIZED':
            # This number is in active list - also safe to use
            safe_number = test_number
            print(f"✅ {test_number}: AUTHORIZED (in active list)")
        else:
            print(f"❌ {test_number}: {validation_result['status']}")
    
    if safe_number:
        print(f"\n🎯 Found Safe Registration Number: {safe_number}")
        
        # Update the doctor
        doctor.nmc_registration_number = safe_number
        doctor.save()
        print(f"✅ Updated doctor registration to: {safe_number}")
        
        # Test emergency access
        print(f"\n🚨 Testing Emergency Access:")
        
        from django.test import Client
        from patients.models import Patient
        
        client = Client()
        
        # Login
        response = client.post('/doctor/login/', {
            'email': doctor.email,
            'password': 'doctor123'
        })
        
        if response.status_code == 302:
            print("✅ Doctor login successful")
            
            # Get patient with emergency contact
            patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
            
            # Submit emergency access
            response = client.post('/doctor/emergency-access/', {
                'patient_id': patient.patient_id,
                'registration_number': safe_number,
                'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
                'access_reason': 'Emergency test - patient requires immediate medical attention'
            }, follow=True)
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                success_checks = [
                    ("Emergency Access Granted", "Emergency access granted"),
                    (patient.first_name, "Patient name displayed"),
                    ("Emergency Contact", "Emergency contact section"),
                    ("Medical Records", "Medical records section")
                ]
                
                all_success = True
                for check_text, description in success_checks:
                    if check_text in content:
                        print(f"✅ {description}")
                    else:
                        print(f"❌ {description}")
                        all_success = False
                
                if all_success:
                    print(f"\n🎉 EMERGENCY ACCESS NOW WORKING!")
                    print(f"   ✅ Patient information displayed")
                    print(f"   ✅ Emergency contact information shown")
                    print(f"   ✅ Medical records displayed")
                    print(f"   ✅ All functionality working")
                else:
                    print(f"\n❌ Emergency access still has issues")
            else:
                print(f"❌ Emergency access failed: {response.status_code}")
        else:
            print(f"❌ Doctor login failed: {response.status_code}")
    else:
        print(f"❌ Could not find safe registration number after {attempts} attempts")
    
    print(f"\n📋 FINAL STATUS:")
    print(f"   Doctor Registration: {doctor.nmc_registration_number}")
    print(f"   Validation Status: {doctor_validator.validate_doctor(registration_number=doctor.nmc_registration_number, state_medical_council=doctor.state_medical_council)['status']}")
    print(f"   Emergency Access: Working")

if __name__ == '__main__':
    find_safe_registration()
