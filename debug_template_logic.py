#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from django.template import Template, Context
from doctors.models import Doctor
from patients.models import Patient

def debug_template_logic():
    """Debug the template logic for emergency access"""
    
    print("🔍 DEBUGGING TEMPLATE LOGIC")
    print("=" * 35)
    
    doctor = Doctor.objects.filter(is_verified=True).first()
    patient = Patient.objects.filter(emergency_contact_name__isnull=False).exclude(emergency_contact_name='').first()
    
    print(f"Doctor: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 TESTING SIMPLE TEMPLATE:")
    print("-" * 35)
    
    # Test simple template with emergency access condition
    template_content = """
    {% if emergency_access_granted and patient %}
        <div class="emergency-info">
            <h3>Emergency Access Granted</h3>
            <p>Patient: {{ patient.first_name }} {{ patient.last_name }}</p>
            <p>Patient ID: {{ patient.patient_id }}</p>
            
            {% if patient.emergency_contact_name %}
                <div class="emergency-contact">
                    <h4>Emergency Contact</h4>
                    <p>Name: {{ patient.emergency_contact_name }}</p>
                    <p>Phone: {{ patient.emergency_contact_phone }}</p>
                    <p>Relation: {{ patient.emergency_contact_relation }}</p>
                </div>
            {% endif %}
            
            {% if patient.medical_records.all %}
                <div class="medical-records">
                    <h4>Medical Records</h4>
                    {% for record in patient.medical_records.all %}
                        <div class="record">
                            <p>Type: {{ record.get_record_type_display }}</p>
                            <p>Title: {{ record.title }}</p>
                            {% if record.file %}
                                <a href="{{ record.file.url }}">Download</a>
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    {% else %}
        <div class="no-access">
            <p>No emergency access granted or no patient data</p>
        </div>
    {% endif %}
    """
    
    template = Template(template_content)
    context = Context({
        'emergency_access_granted': True,
        'patient': patient
    })
    
    rendered = template.render(context)
    
    print(f"\n📄 RENDERED OUTPUT:")
    print("-" * 25)
    print(rendered)
    
    print(f"\n📊 CHECKING OUTPUT:")
    print("-" * 25)
    
    if "Emergency Access Granted" in rendered:
        print(f"✅ Emergency Access Granted: Found")
    else:
        print(f"❌ Emergency Access Granted: NOT found")
    
    if patient.first_name in rendered:
        print(f"✅ Patient Name: Found")
    else:
        print(f"❌ Patient Name: NOT found")
    
    if "Emergency Contact" in rendered:
        print(f"✅ Emergency Contact Section: Found")
    else:
        print(f"❌ Emergency Contact Section: NOT found")
    
    if patient.emergency_contact_name in rendered:
        print(f"✅ Emergency Contact Name: Found")
    else:
        print(f"❌ Emergency Contact Name: NOT found")
    
    if "Medical Records" in rendered:
        print(f"✅ Medical Records Section: Found")
    else:
        print(f"❌ Medical Records Section: NOT found")
    
    records_count = patient.medical_records.count()
    if records_count > 0 and "Download" in rendered:
        print(f"✅ Download Links: Found")
    else:
        print(f"❌ Download Links: NOT found")
    
    print(f"\n🎯 DIAGNOSIS:")
    print("-" * 20)
    
    if "Emergency Access Granted" in rendered:
        print("✅ Template logic is working correctly")
        print("✅ Patient data is being passed correctly")
        print("✅ Emergency contact and medical records should display")
        
        print(f"\n🔧 ISSUE IS IN THE MAIN TEMPLATE:")
        print("-" * 35)
        print("The simple template works, but the main template doesn't.")
        print("This suggests there might be:")
        print("1. CSS hiding the content")
        print("2. JavaScript interfering")
        print("3. Template syntax error")
        print("4. Missing context variables")
    else:
        print("❌ Template logic is not working")
        print("❌ Check emergency_access_granted and patient variables")

if __name__ == '__main__':
    debug_template_logic()
