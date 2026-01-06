#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Doctor
from patients.models import Patient

def check_all_users():
    """Check all users in the system"""
    
    print("🔍 Checking All Users...")
    
    User = get_user_model()
    
    # Check all users
    all_users = User.objects.all()
    print(f"\n👥 Total Users: {all_users.count()}")
    
    for user in all_users:
        print(f"   - {user.email} (is_superuser={user.is_superuser}, is_staff={user.is_staff})")
    
    # Check superusers
    superusers = User.objects.filter(is_superuser=True)
    print(f"\n👑 Superusers: {superusers.count()}")
    
    for user in superusers:
        print(f"   - {user.email} (is_staff={user.is_staff})")
    
    # Check doctors
    doctors = Doctor.objects.all()
    print(f"\n👨‍⚕️ Doctors: {doctors.count()}")
    
    for doctor in doctors:
        print(f"   - {doctor.email} (is_verified={doctor.is_verified}, is_superuser={doctor.is_superuser})")
    
    # Check patients
    patients = Patient.objects.all()
    print(f"\n👩‍⚕️ Patients: {patients.count()}")
    
    for patient in patients:
        print(f"   - {patient.email} (is_superuser={patient.is_superuser})")

if __name__ == '__main__':
    check_all_users()
