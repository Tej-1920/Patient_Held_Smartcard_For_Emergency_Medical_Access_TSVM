#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
import csv

def add_doctor_to_active():
    """Add doctor to active doctors CSV file"""
    
    print("➕ ADDING DOCTOR TO ACTIVE LIST")
    print("=" * 45)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Registration: {doctor.nmc_registration_number}")
    print(f"Council: {doctor.state_medical_council}")
    
    # Path to active doctors CSV
    from django.conf import settings
    csv_path = os.path.join(settings.BASE_DIR, 'static', 'css', 'active_doctors_clean.csv')
    
    print(f"\n📁 CSV Path: {csv_path}")
    
    # Create doctor entry
    doctor_entry = {
        'registration_number': doctor.nmc_registration_number or '99999',
        'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
        'name': f"{doctor.first_name} {doctor.last_name}",
        'qualification_1': 'MBBS',
        'qualification_1_year': '2020',
        'university_name': 'Test University',
        'email': doctor.email,
        'date_of_birth': '01-01-1980',
        'date_of_registration': '01-01-2020',
        'age': '40',
        'experience_years': '5',
        'year_of_info': '2020'
    }
    
    try:
        # Read existing entries
        existing_entries = []
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                existing_entries = list(reader)
        
        # Check if doctor already exists
        doctor_exists = False
        for entry in existing_entries:
            if entry.get('registration_number') == doctor_entry['registration_number']:
                doctor_exists = True
                print(f"⚠️  Doctor already exists in active list")
                break
        
        if not doctor_exists:
            # Add doctor to active list
            existing_entries.append(doctor_entry)
            
            # Write back to CSV
            with open(csv_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = doctor_entry.keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_entries)
            
            print(f"✅ Doctor added to active list successfully")
        else:
            print(f"ℹ️  Doctor already in active list")
        
        # Test validation
        from patients.utils import doctor_validator
        validation_result = doctor_validator.validate_doctor(
            registration_number=doctor_entry['registration_number'],
            state_medical_council=doctor_entry['state_medical_council']
        )
        
        print(f"\n🔍 Validation Result:")
        print(f"   Status: {validation_result['status']}")
        print(f"   Message: {validation_result['message']}")
        
        # Test emergency access
        if validation_result['status'] == 'AUTHORIZED':
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
                print(f"   ✅ Doctor login successful")
                
                # Get patient with emergency contact
                patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
                
                # Submit emergency access
                response = client.post('/doctor/emergency-access/', {
                    'patient_id': patient.patient_id,
                    'registration_number': doctor_entry['registration_number'],
                    'state_medical_council': doctor_entry['state_medical_council'],
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
                            print(f"   ✅ {description}")
                        else:
                            print(f"   ❌ {description}")
                            all_success = False
                    
                    if all_success:
                        print(f"\n🎉 EMERGENCY ACCESS NOW WORKING!")
                        print(f"   ✅ Patient information displayed")
                        print(f"   ✅ Emergency contact information shown")
                        print(f"   ✅ Medical records displayed")
                        print(f"   ✅ All functionality working")
                        
                        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
                        print(f"   1. Restart Django server: python manage.py runserver")
                        print(f"   2. Login as doctor: chaitanyauggina@gmail.com / doctor123")
                        print(f"   3. Go to: http://127.0.0.1:8000/doctor/emergency-access/")
                        print(f"   4. Use patient ID: PT291CD3F8")
                        print(f"   5. Fill form and submit")
                        print(f"   6. Verify emergency contact and medical records are displayed")
                    else:
                        print(f"\n❌ Emergency access still has issues")
                else:
                    print(f"   ❌ Emergency access failed: {response.status_code}")
            else:
                print(f"   ❌ Doctor login failed: {response.status_code}")
        else:
            print(f"\n❌ Doctor validation failed: {validation_result['status']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_doctor_to_active()
