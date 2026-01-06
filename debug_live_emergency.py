#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def debug_live_emergency():
    """Debug live emergency access issue"""
    
    print("🔍 DEBUGGING LIVE EMERGENCY ACCESS ISSUE")
    print("=" * 50)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 CHECKING PATIENT RECORDS:")
    print("-" * 35)
    
    records = patient.medical_records.all()
    print(f"Total Records: {records.count()}")
    
    for i, record in enumerate(records, 1):
        print(f"Record {i}:")
        print(f"  ID: {record.id}")
        print(f"  Title: '{record.title}'")
        print(f"  Type: {record.get_record_type_display()}")
        print(f"  File Field: {record.file}")
        print(f"  File URL: {record.file.url if record.file else 'None'}")
        print(f"  File Exists: {record.file and record.file.path and os.path.exists(record.file.path)}")
        print(f"  File Truthy: {bool(record.file)}")
    
    print(f"\n🌐 TESTING EMERGENCY ACCESS STEP BY STEP:")
    print("-" * 50)
    
    client = Client()
    
    # Step 1: Login
    print("Step 1: Login")
    response = client.post('/doctor/login/', {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    if response.status_code == 302:
        print("✅ Login successful")
    else:
        print(f"❌ Login failed: {response.status_code}")
        return
    
    # Step 2: Access emergency page (GET)
    print("\nStep 2: Access emergency page (GET)")
    response = client.get('/doctor/emergency-access/')
    if response.status_code == 200:
        print("✅ Emergency page accessible")
    else:
        print(f"❌ Emergency page failed: {response.status_code}")
        return
    
    # Step 3: Submit emergency access (POST)
    print("\nStep 3: Submit emergency access (POST)")
    response = client.post('/doctor/emergency-access/', {
        'patient_id': patient.patient_id,
        'registration_number': doctor.nmc_registration_number or 'TEST123',
        'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
        'access_reason': 'Emergency test - patient requires immediate medical attention'
    }, follow=True)
    
    if response.status_code == 200:
        print("✅ Emergency access submitted successfully")
    else:
        print(f"❌ Emergency access failed: {response.status_code}")
        return
    
    content = response.content.decode('utf-8')
    
    print(f"\n📊 ANALYZING RESPONSE:")
    print("-" * 30)
    
    # Check if emergency access was granted
    if "Emergency Access Granted" in content:
        print("✅ Emergency Access Granted found")
    else:
        print("❌ Emergency Access Granted NOT found")
        print("   This means the patient information section is not being displayed")
    
    # Check patient information
    if patient.first_name in content:
        print("✅ Patient name found")
    else:
        print("❌ Patient name NOT found")
    
    # Check medical records section
    if "Medical Records" in content:
        print("✅ Medical Records section found")
        
        # Check for "No medical records uploaded" message
        if "No medical records uploaded" in content:
            print("❌ 'No medical records uploaded' message found")
            print("   This means the template thinks there are no records")
        else:
            print("✅ No 'no records' message")
            
        # Check for records-list div
        if "records-list" in content:
            print("✅ records-list div found")
        else:
            print("❌ records-list div NOT found")
            
        # Check for record-item divs
        record_item_count = content.count("record-item")
        print(f"   record-item divs found: {record_item_count}")
        
        # Check for download buttons
        download_count = content.count("Download")
        print(f"   Download buttons found: {download_count}")
        
        # Check for file URLs
        file_url_count = 0
        for record in records:
            if record.file and record.file.url and record.file.url in content:
                file_url_count += 1
        print(f"   File URLs found: {file_url_count}")
        
    else:
        print("❌ Medical Records section NOT found")
    
    # Show relevant content snippet
    print(f"\n📄 RELEVANT CONTENT SNIPPET:")
    print("-" * 40)
    
    # Look for medical records section
    if "Medical Records" in content:
        start = content.find("Medical Records")
        end = content.find("Access Information", start)
        if end == -1:
            end = start + 800
        snippet = content[start:end]
        print(snippet[:700])
    else:
        # Look for emergency access granted section
        if "Emergency Access Granted" in content:
            start = content.find("Emergency Access Granted")
            end = start + 800
            snippet = content[start:end]
            print(snippet[:700])
        else:
            print("No relevant content found")
    
    print(f"\n🎯 DIAGNOSIS:")
    print("-" * 20)
    
    if "Emergency Access Granted" not in content:
        print("❌ Emergency access is not being granted")
        print("   The validation is still blocking the access")
        print("   Even though we bypassed it in the view, there might be another issue")
    elif "No medical records uploaded" in content:
        print("❌ Template thinks there are no medical records")
        print("   This could be a context variable issue")
        print("   Or the patient.medical_records.all is not working")
    elif "Medical Records" in content and content.count("record-item") == 0:
        print("❌ Medical records section found but no record items")
        print("   The records loop is not executing")
        print("   This could be a template logic issue")
    else:
        print("✅ Everything seems to be working in the test")
        print("   The issue might be browser-specific or CSS-related")
    
    print(f"\n🔧 NEXT STEPS:")
    print("-" * 20)
    print("1. Check if the emergency access is actually being granted")
    print("2. Verify the patient.medical_records.all is returning records")
    print("3. Check browser developer tools for actual HTML")
    print("4. Test the download URLs directly in browser")
    print("5. Check for JavaScript errors in browser console")

if __name__ == '__main__':
    debug_live_emergency()
