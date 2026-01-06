#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor

def check_doctors_status():
    """Check all doctors and their verification status"""
    
    print("🔍 Checking all doctors in database...")
    
    all_doctors = Doctor.objects.all()
    
    if not all_doctors.exists():
        print("❌ No doctors found in database")
        return
    
    print(f"✅ Found {all_doctors.count()} doctors:")
    print()
    
    for doctor in all_doctors:
        print(f"📋 Doctor: {doctor.first_name} {doctor.last_name}")
        print(f"   ID: {doctor.doctor_id}")
        print(f"   Email: {doctor.email}")
        print(f"   Phone: {doctor.phone_number}")
        print(f"   Specialization: {doctor.get_specialization_display()}")
        print(f"   Hospital: {doctor.hospital_name}")
        print(f"   Verification Status: {'✅ Verified' if doctor.is_verified else '⏳ Pending'}")
        print(f"   Created: {doctor.created_at}")
        print(f"   Verification Date: {doctor.verification_date if doctor.verification_date else 'Not verified'}")
        print("-" * 50)
    
    # Count verification status
    verified_count = all_doctors.filter(is_verified=True).count()
    pending_count = all_doctors.filter(is_verified=False).count()
    
    print(f"\n📊 Summary:")
    print(f"   Total Doctors: {all_doctors.count()}")
    print(f"   Verified: {verified_count}")
    print(f"   Pending: {pending_count}")
    
    if pending_count > 0:
        print(f"\n⚠️  {pending_count} doctors are pending verification!")
        print("   These should appear in the admin dashboard pending section.")

if __name__ == '__main__':
    check_doctors_status()
