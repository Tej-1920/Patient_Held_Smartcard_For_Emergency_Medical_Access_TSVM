#!/usr/bin/env python
import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from admin_panel.views import admin_dashboard
from doctors.models import Doctor
from patients.models import Patient

def test_admin_dashboard_view():
    """Test admin dashboard view directly"""
    
    print("🧪 Testing Admin Dashboard View...")
    
    # Get admin user
    User = get_user_model()
    try:
        admin_user = User.objects.get(email='c8projectteam@gmail.com')
        print(f"✅ Found admin user: {admin_user.email}")
    except User.DoesNotExist:
        try:
            admin_user = User.objects.get(email='administrator@system.com')
            print(f"✅ Found admin user: {admin_user.email}")
        except User.DoesNotExist:
            print("❌ Admin user not found")
            return
    
    # Create request factory
    factory = RequestFactory()
    request = factory.get('/admin-panel/')
    request.user = admin_user
    
    try:
        # Call the view
        response = admin_dashboard(request)
        print(f"✅ View executed successfully")
        print(f"   Response status: {response.status_code}")
        
        # Check context
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"\n📊 Context Data:")
            print(f"   total_patients: {context.get('total_patients', 'NOT FOUND')}")
            print(f"   total_doctors: {context.get('total_doctors', 'NOT FOUND')}")
            print(f"   verified_doctors: {context.get('verified_doctors', 'NOT FOUND')}")
            print(f"   pending_doctors: {context.get('pending_doctors', 'NOT FOUND')}")
        else:
            print("❌ No context data found in response")
            
    except Exception as e:
        print(f"❌ Error executing view: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_admin_dashboard_view()
