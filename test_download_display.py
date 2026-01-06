#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.test import Client
from doctors.models import Doctor
from patients.models import Patient

def test_download_display():
    """Test download button display in emergency access"""
    
    print("🔍 TESTING DOWNLOAD BUTTON DISPLAY")
    print("=" * 45)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 MEDICAL RECORDS:")
    print("-" * 25)
    
    records = patient.medical_records.all()
    for i, record in enumerate(records, 1):
        print(f"Record {i}: {record.get_record_type_display()} - {record.title}")
        print(f"  File: {record.file.url if record.file else 'None'}")
    
    print(f"\n🌐 TESTING EMERGENCY ACCESS PAGE:")
    print("-" * 40)
    
    client = Client()
    
    # Login
    response = client.post('/doctor/login/', {
        'email': doctor.email,
        'password': 'doctor123'
    })
    
    if response.status_code == 302:
        print(f"✅ Doctor login successful")
        
        # Submit emergency access
        response = client.post('/doctor/emergency-access/', {
            'patient_id': patient.patient_id,
            'registration_number': doctor.nmc_registration_number or 'TEST123',
            'state_medical_council': doctor.state_medical_council or 'Andhra Pradesh Medical Council',
            'access_reason': 'Emergency test - patient requires immediate medical attention'
        }, follow=True)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            print(f"\n📊 CHECKING DOWNLOAD ELEMENTS:")
            print("-" * 40)
            
            # Check for download buttons
            if "Download" in content:
                print(f"✅ Download button text found")
            else:
                print(f"❌ Download button text NOT found")
            
            # Check for download links
            download_links = []
            for record in records:
                if record.file and record.file.url:
                    if record.file.url in content:
                        print(f"✅ Download URL found: {record.file.url}")
                        download_links.append(record.file.url)
                    else:
                        print(f"❌ Download URL NOT found: {record.file.url}")
            
            # Check for button classes
            if "btn btn-sm btn-outline-primary" in content:
                print(f"✅ Button styling classes found")
            else:
                print(f"❌ Button styling classes NOT found")
            
            # Check for download icon
            if "fa-download" in content:
                print(f"✅ Download icon found")
            else:
                print(f"❌ Download icon NOT found")
            
            # Extract medical records section
            print(f"\n📄 MEDICAL RECORDS SECTION:")
            print("-" * 35)
            
            if "Medical Records" in content:
                start = content.find("Medical Records")
                end = content.find("Access Information", start)
                if end == -1:
                    end = start + 800
                snippet = content[start:end]
                print(snippet[:700])
            else:
                print("Medical Records section not found")
            
            # Check for specific HTML structure
            print(f"\n🔍 HTML STRUCTURE ANALYSIS:")
            print("-" * 40)
            
            # Look for record items
            if "record-item" in content:
                print(f"✅ Record item class found")
            else:
                print(f"❌ Record item class NOT found")
            
            # Look for file condition
            if "{% if record.file %}" in content:
                print(f"❌ Template syntax found in rendered content (should not be there)")
            else:
                print(f"✅ Template syntax properly processed")
            
            # Look for any missing file conditions
            if "No medical records uploaded" in content:
                print(f"❌ 'No medical records uploaded' message shown")
            else:
                print(f"✅ No 'no records' message")
            
            print(f"\n🎯 DIAGNOSIS:")
            print("-" * 20)
            
            if download_links and len(download_links) == records.count():
                print("✅ All download links are present in HTML")
                print("✅ Template is rendering correctly")
                print("🔧 Issue might be:")
                print("   - CSS styling hiding the buttons")
                print("   - JavaScript interfering")
                print("   - Browser rendering issue")
                print("   - Button not visible due to styling")
            else:
                print("❌ Download links missing from HTML")
                print("🔧 Issue might be:")
                print("   - Template logic error")
                print("   - File field not accessible")
                print("   - Context variable issue")
            
            print(f"\n📝 TROUBLESHOOTING STEPS:")
            print("-" * 35)
            print("1. Check browser developer tools")
            print("2. Inspect the download button elements")
            print("3. Check CSS styles applied to buttons")
            print("4. Verify button visibility (display, opacity, etc.)")
            print("5. Test download links directly in browser")
            print("6. Check browser console for JavaScript errors")
        
        else:
            print(f"❌ Emergency access failed: {response.status_code}")
    else:
        print(f"❌ Doctor login failed: {response.status_code}")

if __name__ == '__main__':
    test_download_display()
