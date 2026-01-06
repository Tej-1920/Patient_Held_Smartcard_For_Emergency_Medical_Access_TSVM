#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_known_admin():
    """Create an admin user with known credentials"""
    
    print("🔧 CREATING KNOWN ADMIN USER")
    print("=" * 50)
    
    User = get_user_model()
    
    # Check if admin already exists
    existing_admin = User.objects.filter(email='admin@patientsmartcard.com').first()
    
    if existing_admin:
        print(f"Admin user already exists: {existing_admin.email}")
        print(f"Resetting password to known value...")
        
        # Reset password
        existing_admin.set_password('Admin@123')
        existing_admin.save()
        
        print(f"✅ Password reset successfully!")
        print(f"   Email: admin@patientsmartcard.com")
        print(f"   Password: Admin@123")
        
    else:
        print(f"Creating new admin user...")
        
        # Create new admin
        admin_user = User.objects.create_user(
            email='admin@patientsmartcard.com',
            password='Admin@123',
            first_name='Admin',
            last_name='User',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        
        print(f"✅ Admin user created successfully!")
        print(f"   Email: admin@patientsmartcard.com")
        print(f"   Password: Admin@123")
        print(f"   ID: {admin_user.id}")
    
    # List all admin users
    print(f"\n📋 All Admin Users:")
    print("-" * 25)
    
    admin_users = User.objects.filter(is_superuser=True)
    
    for admin in admin_users:
        print(f"   - {admin.email}")
        print(f"     is_active: {admin.is_active}")
        print(f"     is_superuser: {admin.is_superuser}")
    
    print(f"\n🎯 RECOMMENDED LOGIN:")
    print("-" * 30)
    print(f"   URL: http://127.0.0.1:8000/admin-panel/login/")
    print(f"   Email: admin@patientsmartcard.com")
    print(f"   Password: Admin@123")
    
    print(f"\n✅ ADMIN CREDENTIALS READY!")
    print("=" * 40)
    print(f"   You can now login and test doctor verification")

if __name__ == '__main__':
    create_known_admin()
