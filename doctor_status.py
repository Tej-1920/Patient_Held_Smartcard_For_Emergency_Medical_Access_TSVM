#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor

def check_doctor_status():
    """Check doctor accounts and fix login issues"""
    
    print("👥 DOCTOR STATUS CHECK")
    print("=" * 30)
    
    doctors = Doctor.objects.all()
    print(f"Total Doctors: {doctors.count()}")
    
    for doctor in doctors:
        print(f"\n👨‍⚕️  {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   Doctor ID: {doctor.doctor_id}")
        print(f"   Verified: {'Yes' if doctor.is_verified else 'No'}")
        print(f"   Hospital: {doctor.hospital_name}")
        print(f"   Specialization: {doctor.get_specialization_display()}")
        print(f"   Has Password: {'Yes' if doctor.password else 'No'}")
    
    # Set passwords for doctors if needed
    print(f"\n🔧 SETTING DOCTOR PASSWORDS")
    print("=" * 35)
    
    for doctor in doctors:
        if not doctor.password:
            doctor.set_password('doctor123')
            doctor.save()
            print(f"✅ Password set for {doctor.first_name}")
        else:
            print(f"✅ {doctor.first_name} already has password")
    
    # Verify a doctor for testing
    if doctors.exists():
        test_doctor = doctors.first()
        if not test_doctor.is_verified:
            test_doctor.is_verified = True
            test_doctor.verification_date = timezone.now()
            test_doctor.save()
            print(f"✅ {test_doctor.first_name} verified for testing")
    
    print(f"\n🎯 DOCTOR LOGIN CREDENTIALS")
    print("=" * 35)
    
    for doctor in doctors:
        print(f"\n👨‍⚕️  {doctor.first_name} {doctor.last_name}")
        print(f"   Email: {doctor.email}")
        print(f"   Password: doctor123")
        print(f"   Verified: {'Yes' if doctor.is_verified else 'No'}")
        print(f"   ✅ Ready to login!")
    
    print(f"\n🌐 LOGIN URL:")
    print("http://127.0.0.1:8000/doctor/login/")

if __name__ == '__main__':
    from django.utils import timezone
    check_doctor_status()
