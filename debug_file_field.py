#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient

def debug_file_field():
    """Debug why record.file is evaluating to False"""
    
    print("🔍 DEBUGGING FILE FIELD ISSUE")
    print("=" * 35)
    
    # Get patient with medical records
    patient = Patient.objects.filter(medical_records__isnull=False).first()
    
    if not patient:
        print("❌ No patient with medical records found")
        return
    
    print(f"Patient: {patient.first_name} {patient.last_name} ({patient.patient_id})")
    
    print(f"\n📋 DETAILED RECORD ANALYSIS:")
    print("-" * 40)
    
    records = patient.medical_records.all()
    print(f"Total Records: {records.count()}")
    
    for i, record in enumerate(records, 1):
        print(f"\nRecord {i}:")
        print(f"  ID: {record.id}")
        print(f"  Title: '{record.title}'")
        print(f"  Type: {record.get_record_type_display()}")
        
        # Detailed file field analysis
        print(f"  File Field Analysis:")
        print(f"    record.file: {record.file}")
        print(f"    type(record.file): {type(record.file)}")
        print(f"    bool(record.file): {bool(record.file)}")
        print(f"    record.file is None: {record.file is None}")
        print(f"    record.file == '': {record.file == ''}")
        print(f"    hasattr(record.file, 'url'): {hasattr(record.file, 'url')}")
        
        if record.file:
            print(f"    record.file.name: {record.file.name}")
            print(f"    record.file.url: {record.file.url}")
            print(f"    record.file.path: {record.file.path}")
            print(f"    os.path.exists(record.file.path): {os.path.exists(record.file.path) if record.file.path else 'N/A'}")
            
            # Check if it's a valid FileField
            try:
                file_size = record.file.size
                print(f"    record.file.size: {file_size}")
            except Exception as e:
                print(f"    record.file.size error: {e}")
            
            try:
                file_name = record.file.name
                print(f"    record.file.name: {file_name}")
            except Exception as e:
                print(f"    record.file.name error: {e}")
        else:
            print(f"    ❌ record.file is falsy")
        
        # Test template condition simulation
        print(f"  Template Condition Simulation:")
        if record.file:
            print(f"    ✅ {{% if record.file %}} would be True")
        else:
            print(f"    ❌ {{% if record.file %}} would be False")
        
        # Test different conditions
        print(f"  Alternative Conditions:")
        if record.file and record.file.name:
            print(f"    ✅ {{% if record.file and record.file.name %}} would be True")
        else:
            print(f"    ❌ {{% if record.file and record.file.name %}} would be False")
        
        if hasattr(record, 'file') and record.file:
            print(f"    ✅ {{% if hasattr(record, 'file') and record.file %}} would be True")
        else:
            print(f"    ❌ {{% if hasattr(record, 'file') and record.file %}} would be False")
    
    print(f"\n🔧 POSSIBLE SOLUTIONS:")
    print("-" * 30)
    print("1. Check if record.file.name exists instead of record.file")
    print("2. Use {% if record.file.name %} condition")
    print("3. Use {% if record.file and record.file.url %} condition")
    print("4. Check for empty string vs None")
    print("5. Use {% if record.file %} with additional checks")
    
    print(f"\n📝 RECOMMENDED TEMPLATE FIX:")
    print("-" * 35)
    print("Change:")
    print("  {% if record.file %}")
    print("To:")
    print("  {% if record.file and record.file.name %}")
    print("Or:")
    print("  {% if record.file.url %}")

if __name__ == '__main__':
    debug_file_field()
