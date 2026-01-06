#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

def make_existing_user_superuser():
    """Make the existing c8projectteam user a superuser"""
    
    try:
        # Try to find the existing user
        user = Patient.objects.get(email='c8projectteam@gmail.com')
        
        # Make them a superuser
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        print(f"✅ Successfully made {user.email} a superuser!")
        print(f"   Name: {user.first_name} {user.last_name}")
        print(f"   Phone: {user.phone_number}")
        print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")
        print(f"   Use your existing password to login")
        
    except Patient.DoesNotExist:
        print("❌ User c8projectteam@gmail.com not found")
        
        # Try to create a new superuser with different phone
        try:
            print("🔄 Creating new superuser with different phone number...")
            admin_user = Patient.objects.create_superuser(
                email='admin@patientsmartcard.com',
                password='Admin@123',
                first_name='System',
                last_name='Administrator',
                phone_number='9999999999'  # Different phone number
            )
            print(f"✅ New superuser created!")
            print(f"   Email: admin@patientsmartcard.com")
            print(f"   Password: Admin@123")
            print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")
            
        except Exception as e:
            print(f"❌ Error creating new superuser: {e}")

if __name__ == '__main__':
    make_existing_user_superuser()
