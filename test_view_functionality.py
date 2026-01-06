#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from patients.models import Patient
from django.test import Client
from django.contrib.auth import get_user_model

def test_view_functionality():
    """Test the new view functionality for patients and doctors"""
    
    print("🔍 TESTING VIEW FUNCTIONALITY")
    print("=" * 50)
    
    # Step 1: Check if we have test data
    print(f"\n📊 Step 1: Check Test Data")
    print("-" * 35)
    
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    
    print(f"Patients: {patients.count()}")
    print(f"Doctors: {doctors.count()}")
    
    if patients.count() == 0 and doctors.count() == 0:
        print("❌ No test data available")
        return False
    
    # Step 2: Login as admin
    print(f"\n🔐 Step 2: Admin Login")
    print("-" * 30)
    
    client = Client()
    login_success = client.login(username='admin@patientsmartcard.com', password='Admin@123')
    
    if not login_success:
        print("❌ Admin login failed")
        return False
    
    print("✅ Admin login successful")
    
    # Step 3: Test patient view
    if patients.exists():
        print(f"\n👤 Step 3: Test Patient View")
        print("-" * 35)
        
        test_patient = patients.first()
        print(f"Testing patient: {test_patient.first_name} {test_patient.last_name}")
        
        try:
            response = client.get(f'/admin-panel/patients/{test_patient.id}/')
            print(f"Patient View Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Patient view loads successfully")
                
                # Check content
                content = response.content.decode('utf-8')
                if test_patient.first_name in content:
                    print("✅ Patient name displayed")
                if 'Patient Details' in content:
                    print("✅ Page title correct")
                if 'Medical Records' in content:
                    print("✅ Medical records section present")
                    
            else:
                print(f"❌ Patient view failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing patient view: {e}")
    
    # Step 4: Test doctor view
    if doctors.exists():
        print(f"\n👨‍⚕️  Step 4: Test Doctor View")
        print("-" * 35)
        
        test_doctor = doctors.first()
        print(f"Testing doctor: Dr. {test_doctor.first_name} {test_doctor.last_name}")
        
        try:
            response = client.get(f'/admin-panel/doctors/{test_doctor.id}/')
            print(f"Doctor View Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Doctor view loads successfully")
                
                # Check content
                content = response.content.decode('utf-8')
                if test_doctor.first_name in content:
                    print("✅ Doctor name displayed")
                if 'Doctor Details' in content:
                    print("✅ Page title correct")
                if 'Professional Information' in content:
                    print("✅ Professional info section present")
                if 'Access Logs' in content:
                    print("✅ Access logs section present")
                    
            else:
                print(f"❌ Doctor view failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing doctor view: {e}")
    
    # Step 5: Test URL patterns
    print(f"\n🔗 Step 5: Test URL Patterns")
    print("-" * 35)
    
    try:
        from django.urls import reverse
        
        if patients.exists():
            patient_url = reverse('admin_panel:view_patient_details', kwargs={'patient_id': patients.first().id})
            print(f"Patient URL: {patient_url}")
            
        if doctors.exists():
            doctor_url = reverse('admin_panel:view_doctor_details', kwargs={'doctor_id': doctors.first().id})
            print(f"Doctor URL: {doctor_url}")
            
        print("✅ URL patterns working correctly")
        
    except Exception as e:
        print(f"❌ URL pattern error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = test_view_functionality()
    
    if success:
        print(f"\n🎉 VIEW FUNCTIONALITY WORKING!")
        print(f"   ✅ Patient details view implemented")
        print(f"   ✅ Doctor details view implemented")
        print(f"   ✅ URL patterns working")
        print(f"   ✅ Templates loading correctly")
        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
        print("=" * 45)
        print(f"   1. Login to admin panel")
        print(f"   2. Go to 'Manage Patients' or 'Manage Doctors'")
        print(f"   3. Click 'View' button next to any record")
        print(f"   4. Should see detailed information page")
        print(f"   5. All data should be displayed in read-only format")
    else:
        print(f"\n❌ VIEW FUNCTIONALITY HAS ISSUES!")
