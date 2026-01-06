#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from django.utils import timezone

def create_verified_doctor():
    """Create a verified doctor for testing"""
    
    print("🔧 Creating Verified Doctor...")
    
    try:
        # Create verified doctor
        doctor = Doctor.objects.create_user(
            email='verified.doctor@example.com',
            password='Test@123',
            first_name='Verified',
            last_name='Doctor',
            phone_number='9876543212',
            nmc_registration_number='VERIFIED123',
            specialization='CARDIOLOGY',
            hospital_name='Verified Hospital',
            hospital_address='456 Verified Street',
            years_of_experience=15,
            medical_license_number='MLVERIFIED123',
            state_medical_council='Tamil Nadu Medical Council'
        )
        
        # Mark as verified
        doctor.is_verified = True
        doctor.verification_date = timezone.now()
        doctor.save()
        
        print(f"✅ Verified doctor created successfully!")
        print(f"   Email: verified.doctor@example.com")
        print(f"   Password: Test@123")
        print(f"   Verification Status: Verified")
        print(f"   Doctor ID: {doctor.doctor_id}")
        print(f"   Verification Date: {doctor.verification_date}")
        
    except Exception as e:
        print(f"❌ Error creating verified doctor: {e}")

if __name__ == '__main__':
    create_verified_doctor()
