#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_fresh_admin():
    """Create a fresh admin user with known credentials"""
    
    print("🔧 Creating Fresh Admin User...")
    
    User = get_user_model()
    
    # Delete existing admin if exists
    try:
        existing = User.objects.get(email='admin@patientsmartcard.com')
        existing.delete()
        print("   Deleted existing admin user")
    except User.DoesNotExist:
        pass
    
    # Create new admin
    try:
        admin = User.objects.create_superuser(
            email='admin@patientsmartcard.com',
            password='Admin@123',
            first_name='Admin',
            last_name='User'
        )
        print(f"✅ Fresh admin user created!")
        print(f"   Email: admin@patientsmartcard.com")
        print(f"   Password: Admin@123")
        print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")
        
    except Exception as e:
        print(f"❌ Error creating admin: {e}")

if __name__ == '__main__':
    create_fresh_admin()
