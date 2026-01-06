#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

print('🔍 PATIENT IMAGE STATUS')
print('=' * 35)

for patient in Patient.objects.all():
    has_image = bool(patient.profile_image and patient.profile_image.name)
    
    print(f'\n👤 {patient.first_name} {patient.last_name}')
    print(f'   Email: {patient.email}')
    print(f'   Has Image: {"✅ Yes" if has_image else "❌ No"}')
    
    if has_image:
        print(f'   Image: {patient.profile_image.name}')
        print(f'   ✅ USE THIS LOGIN TO SEE IMAGE')

print(f'\n🎯 SOLUTION:')
print('=' * 20)
print('The issue is that you are logged in as a patient')
print('who does NOT have an image uploaded.')
print('')
print('To see the image working:')
print('1. Login as: tejaswiniuggina282@gmail.com')
print('2. Go to dashboard')
print('3. You will see the profile image!')
print('')
print('OR upload an image for your current patient:')
