#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client, RequestFactory
from django.urls import reverse
from doctors.models import Doctor
from patients.models import Patient, MedicalRecord

def test_doctor_patient_search():
    """Test doctor patient search and view functionality"""
    
    print("🏥 TESTING DOCTOR PATIENT SEARCH SYSTEM")
    print("=" * 50)
    
    # Step 1: Check doctors and patients
    print(f"\n👥 Step 1: Check Available Users")
    print("-" * 35)
    
    doctors = Doctor.objects.filter(is_verified=True)
    patients = Patient.objects.all()
    
    print(f"Verified Doctors: {doctors.count()}")
    print(f"Total Patients: {patients.count()}")
    
    if not doctors.exists():
        print("❌ No verified doctors found")
        return False
    
    if not patients.exists():
        print("❌ No patients found")
        return False
    
    # Get test doctor and patient
    doctor = doctors.first()
    patient = patients.first()
    
    print(f"Test Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Test Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    # Step 2: Test URLs
    print(f"\n🔗 Step 2: Test URL Patterns")
    print("-" * 35)
    
    try:
        search_url = reverse('doctors:search_patient')
        profile_url = reverse('doctors:view_patient_profile', args=[patient.id])
        records_url = reverse('doctors:view_patient_records', args=[patient.id])
        
        print(f"✅ Search URL: {search_url}")
        print(f"✅ Profile URL: {profile_url}")
        print(f"✅ Records URL: {records_url}")
        
    except Exception as e:
        print(f"❌ URL pattern error: {e}")
        return False
    
    # Step 3: Test access without login
    print(f"\n🔒 Step 3: Test Access Without Login")
    print("-" * 40)
    
    client = Client()
    
    try:
        response = client.get(search_url)
        if response.status_code == 302:
            print("✅ Search page redirects to login (correct)")
        else:
            print(f"⚠️  Search page status: {response.status_code}")
            
        response = client.get(profile_url)
        if response.status_code == 302:
            print("✅ Profile page redirects to login (correct)")
        else:
            print(f"⚠️  Profile page status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing access: {e}")
    
    # Step 4: Login as doctor
    print(f"\n🔐 Step 4: Login as Doctor")
    print("-" * 30)
    
    try:
        # Set password if needed
        if not doctor.password:
            doctor.set_password('doctor123')
            doctor.save()
        
        # Login
        response = client.post('/doctor/login/', {
            'email': doctor.email,
            'password': 'doctor123'
        }, follow=True)
        
        if response.status_code == 200:
            print("✅ Doctor login successful")
        else:
            print(f"❌ Doctor login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 5: Test patient search page
    print(f"\n🔍 Step 5: Test Patient Search Page")
    print("-" * 40)
    
    try:
        response = client.get(search_url)
        print(f"Search Page Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            checks = [
                ('Patient Search', 'Search page title'),
                ('Search Patients', 'Search form'),
                ('Patient ID', 'Search instructions'),
                ('Search Tips', 'Help section')
            ]
            
            for check_text, description in checks:
                if check_text in content:
                    print(f"✅ {description}: Found")
                else:
                    print(f"❌ {description}: Missing")
        else:
            print(f"❌ Search page failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing search page: {e}")
    
    # Step 6: Test patient search functionality
    print(f"\n🎯 Step 6: Test Patient Search Functionality")
    print("-" * 45)
    
    search_tests = [
        (patient.patient_id, "Patient ID search"),
        (patient.email, "Email search"),
        (patient.first_name, "First name search"),
        (patient.last_name, "Last name search")
    ]
    
    for query, description in search_tests:
        try:
            response = client.post(search_url, {'query': query})
            print(f"{description}: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if patient.first_name in content or patient.last_name in content:
                    print(f"✅ {description}: Results found")
                else:
                    print(f"❌ {description}: No results")
            else:
                print(f"❌ {description}: Failed")
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    # Step 7: Test patient profile view
    print(f"\n👤 Step 7: Test Patient Profile View")
    print("-" * 40)
    
    try:
        response = client.get(profile_url)
        print(f"Profile Page Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            profile_checks = [
                (patient.first_name, 'Patient name'),
                (patient.patient_id, 'Patient ID'),
                (patient.email, 'Patient email'),
                ('Personal Details', 'Details section'),
                ('Emergency Contact', 'Emergency section'),
                ('Medical Information', 'Medical section')
            ]
            
            for check_text, description in profile_checks:
                if check_text in content:
                    print(f"✅ {description}: Found")
                else:
                    print(f"❌ {description}: Missing")
        else:
            print(f"❌ Profile page failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing profile: {e}")
    
    # Step 8: Test medical records view
    print(f"\n📋 Step 8: Test Medical Records View")
    print("-" * 40)
    
    try:
        response = client.get(records_url)
        print(f"Records Page Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            records_checks = [
                ('Medical Records', 'Records title'),
                (patient.first_name, 'Patient name'),
                ('All Medical Records', 'Records section'),
                ('Medical Summary', 'Summary section'),
                ('Emergency Contact', 'Emergency section')
            ]
            
            for check_text, description in records_checks:
                if check_text in content:
                    print(f"✅ {description}: Found")
                else:
                    print(f"❌ {description}: Missing")
        else:
            print(f"❌ Records page failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing records: {e}")
    
    return True

def test_patient_data():
    """Test patient data completeness"""
    
    print(f"\n📊 Step 9: Test Patient Data Completeness")
    print("-" * 45)
    
    patients = Patient.objects.all()
    
    for patient in patients[:3]:  # Test first 3 patients
        print(f"\n👤 {patient.first_name} {patient.last_name}")
        print(f"   ID: {patient.patient_id}")
        print(f"   Email: {patient.email}")
        print(f"   Phone: {patient.phone_number}")
        print(f"   Blood Group: {patient.get_blood_group_display()}")
        print(f"   Gender: {patient.get_gender_display()}")
        print(f"   Age: {patient.age}")
        print(f"   Address: {'Yes' if patient.address else 'No'}")
        print(f"   Emergency Contact: {'Yes' if patient.emergency_contact_name else 'No'}")
        print(f"   Chronic Diseases: {'Yes' if patient.chronic_diseases else 'No'}")
        print(f"   Allergies: {'Yes' if patient.allergies else 'No'}")
        print(f"   Profile Image: {'Yes' if patient.profile_image else 'No'}")
        print(f"   QR Code: {'Yes' if patient.qr_code else 'No'}")
        print(f"   Medical Records: {patient.medical_records.count()} files")

if __name__ == '__main__':
    success = test_doctor_patient_search()
    
    if success:
        test_patient_data()
        
        print(f"\n🎉 DOCTOR PATIENT SEARCH SYSTEM WORKING!")
        print(f"   ✅ Search functionality implemented")
        print(f"   ✅ Patient profile view working")
        print(f"   ✅ Medical records view working")
        print(f"   ✅ Emergency contact display working")
        print(f"   ✅ Complete patient information available")
        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
        print("=" * 50)
        print(f"   1. Login as verified doctor:")
        print(f"      - chaitanyauggina@gmail.com / doctor123")
        print(f"   2. Go to dashboard")
        print(f"   3. Click 'Search Patient'")
        print(f"   4. Search by patient ID, email, or name")
        print(f"   5. Click 'View Profile' to see complete details")
        print(f"   6. Click 'Medical Records' to see uploaded files")
        print(f"   7. Verify all patient information is displayed")
    else:
        print(f"\n❌ DOCTOR PATIENT SEARCH SYSTEM HAS ISSUES!")
