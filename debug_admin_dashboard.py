#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from patients.models import Patient
from patients.utils import doctor_validator

def debug_admin_dashboard():
    """Debug admin dashboard data"""
    
    print("🔍 Debugging Admin Dashboard Data...")
    
    # Check all doctors
    all_doctors = Doctor.objects.all()
    print(f"\n📊 Total Doctors in DB: {all_doctors.count()}")
    
    for doctor in all_doctors:
        print(f"   - {doctor.first_name} {doctor.last_name}: is_verified={doctor.is_verified}")
    
    # Check pending doctors
    pending_doctors = Doctor.objects.filter(is_verified=False)
    print(f"\n⏳ Pending Doctors: {pending_doctors.count()}")
    
    for doctor in pending_doctors:
        print(f"   - {doctor.first_name} {doctor.last_name} ({doctor.email})")
    
    # Check verified doctors
    verified_doctors = Doctor.objects.filter(is_verified=True)
    print(f"\n✅ Verified Doctors: {verified_doctors.count()}")
    
    for doctor in verified_doctors:
        print(f"   - {doctor.first_name} {doctor.last_name} ({doctor.email})")
    
    # Check patients
    patients = Patient.objects.all()
    print(f"\n👥 Patients: {patients.count()}")
    
    # Check validation stats
    try:
        validation_stats = doctor_validator.get_statistics()
        print(f"\n📈 Validation Stats: {validation_stats}")
    except Exception as e:
        print(f"\n❌ Validation Stats Error: {e}")
    
    # Simulate admin dashboard calculation
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    verified_doctors_count = Doctor.objects.filter(is_verified=True).count()
    pending_doctors_count = Doctor.objects.filter(is_verified=False).count()
    
    print(f"\n🎯 Admin Dashboard Calculation:")
    print(f"   total_patients: {total_patients}")
    print(f"   total_doctors: {total_doctors}")
    print(f"   verified_doctors: {verified_doctors_count}")
    print(f"   pending_doctors: {pending_doctors_count}")
    
    # Check if there's a caching issue
    print(f"\n🔄 Checking for potential issues...")
    
    # Check if any doctors have None as is_verified
    none_verified = Doctor.objects.filter(is_verified__isnull=True)
    if none_verified.exists():
        print(f"   ⚠️  Found {none_verified.count()} doctors with is_verified=None")
        for doctor in none_verified:
            print(f"      - {doctor.first_name} {doctor.last_name}")
    
    # Check if any doctors have is_verified=False but it's not being counted
    false_verified = Doctor.objects.filter(is_verified=False)
    print(f"   📋 Doctors with is_verified=False: {false_verified.count()}")
    for doctor in false_verified:
        print(f"      - {doctor.first_name} {doctor.last_name} (is_verified={doctor.is_verified})")

if __name__ == '__main__':
    debug_admin_dashboard()
