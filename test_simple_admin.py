#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Doctor
from patients.models import Patient

def test_simple_admin():
    """Test admin dashboard calculation directly"""
    
    print("🧪 Testing Admin Dashboard Calculation...")
    
    # Simulate the admin dashboard view calculation
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    verified_doctors = Doctor.objects.filter(is_verified=True).count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    
    print(f"\n📊 Direct Calculation Results:")
    print(f"   total_patients: {total_patients}")
    print(f"   total_doctors: {total_doctors}")
    print(f"   verified_doctors: {verified_doctors}")
    print(f"   pending_doctors: {pending_doctors}")
    
    # Check if the condition would be true
    if pending_doctors > 0:
        print(f"\n✅ Condition 'pending_doctors > 0' is TRUE")
        print(f"   The pending verification section should be displayed")
    else:
        print(f"\n❌ Condition 'pending_doctors > 0' is FALSE")
        print(f"   The pending verification section should NOT be displayed")
    
    # Check each doctor's verification status
    print(f"\n👨‍⚕️ Doctor Details:")
    for doctor in Doctor.objects.all():
        print(f"   - {doctor.first_name} {doctor.last_name}")
        print(f"     Email: {doctor.email}")
        print(f"     is_verified: {doctor.is_verified}")
        print(f"     is_verified type: {type(doctor.is_verified)}")
        print(f"     is_verified == False: {doctor.is_verified == False}")
        print(f"     is_verified == True: {doctor.is_verified == True}")

if __name__ == '__main__':
    test_simple_admin()
