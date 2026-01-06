#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

def create_super_user():
    """Create a superuser for the admin panel"""
    
    # Admin details
    email = 'admin@patientsmartcard.com'
    password = 'Admin@123'  # You can change this
    first_name = 'System'
    last_name = 'Administrator'
    phone_number = '9999999999'  # Unique phone number
    
    try:
        # Check if user already exists
        if Patient.objects.filter(email=email).exists():
            user = Patient.objects.get(email=email)
            print(f"✅ Admin user {email} already exists!")
            print(f"   Current password: {password}")
            print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")
            return
        
        # Create superuser
        admin_user = Patient.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        
        print(f"✅ Superuser created successfully!")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        
        # Try alternative method
        try:
            print("🔄 Trying alternative method...")
            # Check if c8projectteam user exists and make it superuser
            user = Patient.objects.get(email='c8projectteam@gmail.com')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"✅ Made {user.email} a superuser!")
            print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")
        except Patient.DoesNotExist:
            print("❌ Could not find c8projectteam@gmail.com user")
        except Exception as e2:
            print(f"❌ Alternative method failed: {e2}")

if __name__ == '__main__':
    create_super_user()
