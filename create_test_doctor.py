#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor

def create_test_doctor():
    """Create a test doctor for verification testing"""
    
    try:
        # Check if test doctor already exists
        if Doctor.objects.filter(email='test.doctor@example.com').exists():
            print("✅ Test doctor already exists")
            return
        
        # Create test doctor
        doctor = Doctor.objects.create_user(
            email='test.doctor@example.com',
            password='Test@123',
            first_name='Test',
            last_name='Doctor',
            phone_number='9876543210',
            nmc_registration_number='TEST123456',
            specialization='General Practice',
            hospital_name='Test Hospital',
            hospital_address='123 Test Street',
            years_of_experience=5,
            medical_license_number='ML123456',
            state_medical_council='Andhra Pradesh Medical Council'
        )
        
        print(f"✅ Test doctor created successfully!")
        print(f"   Email: test.doctor@example.com")
        print(f"   Password: Test@123")
        print(f"   Verification Status: {'Verified' if doctor.is_verified else 'Pending'}")
        print(f"   Doctor ID: {doctor.doctor_id}")
        
    except Exception as e:
        print(f"❌ Error creating test doctor: {e}")

if __name__ == '__main__':
    create_test_doctor()
