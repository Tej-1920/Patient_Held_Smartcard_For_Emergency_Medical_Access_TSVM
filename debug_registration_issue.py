#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from admin_panel.views import admin_dashboard

def debug_registration_issue():
    """Debug why registered doctors don't appear in admin panel"""
    
    print("🔍 DEBUGGING REGISTRATION ISSUE")
    print("=" * 50)
    
    # Step 1: Check all doctors in database
    print(f"\n📊 STEP 1: Database Check")
    print("-" * 30)
    
    all_doctors = Doctor.objects.all()
    print(f"Total Doctors in DB: {all_doctors.count()}")
    
    if all_doctors.exists():
        for doctor in all_doctors:
            print(f"\n👨‍⚕️  Doctor: {doctor.first_name} {doctor.last_name}")
            print(f"   Email: {doctor.email}")
            print(f"   Phone: {doctor.phone_number}")
            print(f"   NMC: {doctor.nmc_registration_number}")
            print(f"   Hospital: {doctor.hospital_name}")
            print(f"   is_verified: {doctor.is_verified}")
            print(f"   Created: {doctor.created_at}")
            print(f"   Doctor ID: {doctor.doctor_id}")
    else:
        print("❌ No doctors found in database!")
    
    # Step 2: Check pending doctors specifically
    print(f"\n📋 STEP 2: Pending Doctors Check")
    print("-" * 30)
    
    pending_doctors = Doctor.objects.filter(is_verified=False)
    print(f"Pending Doctors: {pending_doctors.count()}")
    
    if pending_doctors.exists():
        for doctor in pending_doctors:
            print(f"   - Dr. {doctor.first_name} {doctor.last_name} ({doctor.email})")
    else:
        print("❌ No pending doctors found!")
    
    # Step 3: Simulate admin dashboard calculation
    print(f"\n🏢 STEP 3: Admin Dashboard Calculation")
    print("-" * 30)
    
    try:
        # Simulate the admin dashboard logic
        total_patients = 0  # We'll check this later
        total_doctors = Doctor.objects.count()
        verified_doctors = Doctor.objects.filter(is_verified=True).count()
        pending_doctors = Doctor.objects.filter(is_verified=False).count()
        
        print(f"Admin Dashboard Should Show:")
        print(f"   Total Patients: {total_patients}")
        print(f"   Total Doctors: {total_doctors}")
        print(f"   Verified Doctors: {verified_doctors}")
        print(f"   Pending Doctors: {pending_doctors}")
        
        if pending_doctors > 0:
            print(f"   ✅ Should show '{pending_doctors} Doctors awaiting verification'")
        else:
            print(f"   ❌ Should show '0 Doctors awaiting verification'")
            
    except Exception as e:
        print(f"❌ Error in dashboard calculation: {e}")
    
    # Step 4: Check recent registrations
    print(f"\n🕐 STEP 4: Recent Registrations")
    print("-" * 30)
    
    from django.utils import timezone
    from datetime import timedelta
    
    recent_time = timezone.now() - timedelta(minutes=30)
    recent_doctors = Doctor.objects.filter(created_at__gte=recent_time)
    
    print(f"Registrations in last 30 minutes: {recent_doctors.count()}")
    
    if recent_doctors.exists():
        for doctor in recent_doctors:
            print(f"   - Dr. {doctor.first_name} {doctor.last_name}")
            print(f"     Email: {doctor.email}")
            print(f"     Created: {doctor.created_at}")
            print(f"     is_verified: {doctor.is_verified}")
    
    # Step 5: Check if there are any issues with the admin user
    print(f"\n👤 STEP 5: Admin User Check")
    print("-" * 30)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    admin_users = User.objects.filter(is_superuser=True)
    print(f"Admin Users: {admin_users.count()}")
    
    for admin in admin_users:
        print(f"   - {admin.email} (is_superuser: {admin.is_superuser})")
    
    # Step 6: Test the actual admin dashboard view
    print(f"\n🔧 STEP 6: Test Admin Dashboard View")
    print("-" * 30)
    
    try:
        # Create a mock request for testing
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/admin-panel/')
        
        # Get the first admin user
        admin_user = admin_users.first()
        if admin_user:
            request.user = admin_user
            
            # Call the admin dashboard view
            context = admin_dashboard(request)
            
            if hasattr(context, 'context_data'):
                context_data = context.context_data
                print(f"Admin Dashboard Context:")
                print(f"   total_patients: {context_data.get('total_patients', 'N/A')}")
                print(f"   total_doctors: {context_data.get('total_doctors', 'N/A')}")
                print(f"   verified_doctors: {context_data.get('verified_doctors', 'N/A')}")
                print(f"   pending_doctors: {context_data.get('pending_doctors', 'N/A')}")
            else:
                print(f"❌ No context data found in response")
        else:
            print(f"❌ No admin user found for testing")
            
    except Exception as e:
        print(f"❌ Error testing admin dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_registration_issue()
