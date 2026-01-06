#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

def check_and_create_admin():
    """Check existing users and create admin"""
    
    print("🔍 Checking existing users...")
    all_users = Patient.objects.all()
    
    for user in all_users:
        print(f"   - {user.email} (Phone: {user.phone_number}, Superuser: {user.is_superuser})")
    
    # Try to create admin with unique data
    try:
        print("\n🔄 Creating admin user...")
        admin_user = Patient.objects.create_superuser(
            email='administrator@system.com',
            password='Admin@123',
            first_name='System',
            last_name='Admin',
            phone_number='8888888888'  # Unique phone
        )
        print(f"✅ Admin user created successfully!")
        print(f"   Email: administrator@system.com")
        print(f"   Password: Admin@123")
        print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Alternative: make first user superuser
        if all_users.exists():
            first_user = all_users.first()
            first_user.is_staff = True
            first_user.is_superuser = True
            first_user.save()
            print(f"✅ Made {first_user.email} a superuser!")
            print(f"   Use existing password to login")
            print(f"   Login URL: http://127.0.0.1:8000/admin-panel/login/")

if __name__ == '__main__':
    check_and_create_admin()
