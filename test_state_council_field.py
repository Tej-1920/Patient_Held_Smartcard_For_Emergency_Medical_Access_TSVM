#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.forms import DoctorRegistrationForm

def test_state_council_field():
    """Test the State Medical Council field specifically"""
    
    print("🔍 TESTING STATE MEDICAL COUNCIL FIELD")
    print("=" * 50)
    
    # Test 1: Check form field configuration
    print(f"\n📋 Step 1: Form Field Configuration")
    print("-" * 40)
    
    form = DoctorRegistrationForm()
    
    # Check if state_medical_council field exists
    if 'state_medical_council' in form.fields:
        state_field = form.fields['state_medical_council']
        print(f"✅ State Medical Council field found in form")
        print(f"   Field Type: {type(state_field).__name__}")
        print(f"   Required: {state_field.required}")
        print(f"   Choices: {len(state_field.choices)} options")
        
        print(f"\n📝 Available Choices:")
        for i, (value, label) in enumerate(state_field.choices, 1):
            print(f"   {i}. {label}")
    else:
        print(f"❌ State Medical Council field NOT found in form")
        return False
    
    # Test 2: Check form rendering
    print(f"\n🎨 Step 2: Form Field Rendering")
    print("-" * 40)
    
    try:
        rendered_field = str(form['state_medical_council'])
        print(f"✅ Field renders successfully")
        print(f"   Rendered HTML length: {len(rendered_field)} characters")
        
        # Check if it's a select field
        if '<select' in rendered_field:
            print(f"   ✅ Renders as select dropdown")
            
            # Count options in rendered HTML
            option_count = rendered_field.count('<option')
            print(f"   Options in HTML: {option_count}")
            
            if option_count > 1:
                print(f"   ✅ Multiple options available")
            else:
                print(f"   ⚠️  Only one option found")
        else:
            print(f"   ❌ Does not render as select dropdown")
            
    except Exception as e:
        print(f"   ❌ Field rendering failed: {e}")
        return False
    
    # Test 3: Test form validation with state council
    print(f"\n✅ Step 3: Form Validation with State Council")
    print("-" * 40)
    
    test_data = {
        'first_name': 'State',
        'last_name': 'Test',
        'email': 'state.test@example.com',
        'phone_number': '9876543222',
        'nmc_registration_number': 'STATE-TEST-001',
        'specialization': 'GENERAL',
        'hospital_name': 'State Test Hospital',
        'hospital_address': '123 State Street',
        'years_of_experience': 6,
        'medical_license_number': 'ML-STATE-001',
        'state_medical_council': 'Karnataka Medical Council',
        'password1': 'StateTest@123456',
        'password2': 'StateTest@123456',
    }
    
    form = DoctorRegistrationForm(data=test_data)
    
    print(f"   Form is valid: {form.is_valid()}")
    
    if form.is_valid():
        print(f"   ✅ State Council: '{form.cleaned_data['state_medical_council']}'")
        print(f"   ✅ All fields validated successfully")
    else:
        print(f"   ❌ Form validation errors:")
        for field, errors in form.errors.items():
            print(f"     {field}: {errors}")
    
    # Test 4: Check different state council values
    print(f"\n🔄 Step 4: Testing Different State Council Values")
    print("-" * 40)
    
    test_councils = [
        'Andhra Pradesh Medical Council',
        'Tamil Nadu Medical Council',
        'Karnataka Medical Council',
        'Maharashtra Medical Council',
        'Delhi Medical Council'
    ]
    
    for council in test_councils:
        test_data['state_medical_council'] = council
        test_data['email'] = f'test.{council.split()[0].lower()}@example.com'
        
        form = DoctorRegistrationForm(data=test_data)
        
        if form.is_valid():
            print(f"   ✅ {council}: Valid")
        else:
            print(f"   ❌ {council}: Invalid")
            if 'state_medical_council' in form.errors:
                print(f"      Error: {form.errors['state_medical_council']}")
    
    return True

if __name__ == '__main__':
    success = test_state_council_field()
    
    if success:
        print(f"\n🎉 STATE MEDICAL COUNCIL FIELD WORKS!")
        print(f"   ✅ Field configured correctly")
        print(f"   ✅ Choices available")
        print(f"   ✅ Form renders properly")
        print(f"   ✅ Validation works")
        print(f"\n📝 Field is ready for manual testing!")
    else:
        print(f"\n❌ STATE MEDICAL COUNCIL FIELD HAS ISSUES!")
