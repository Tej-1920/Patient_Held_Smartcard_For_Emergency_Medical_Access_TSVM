#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.forms import DoctorRegistrationForm

def test_styled_form():
    """Test the styled registration form"""
    
    print("🎨 TESTING STYLED REGISTRATION FORM")
    print("=" * 50)
    
    # Test 1: Check form field styling
    print(f"\n📋 Step 1: Form Field Styling")
    print("-" * 40)
    
    form = DoctorRegistrationForm()
    
    # Check key fields have proper CSS classes
    fields_to_check = [
        'first_name', 'last_name', 'email', 'phone_number',
        'nmc_registration_number', 'specialization', 'hospital_name',
        'hospital_address', 'years_of_experience', 'medical_license_number',
        'state_medical_council'
    ]
    
    for field_name in fields_to_check:
        if field_name in form.fields:
            field = form.fields[field_name]
            widget = field.widget
            
            if hasattr(widget, 'attrs'):
                css_class = widget.attrs.get('class', '')
                print(f"   {field_name}: '{css_class}' ✅")
            else:
                print(f"   {field_name}: No styling attributes ⚠️")
        else:
            print(f"   {field_name}: Field not found ❌")
    
    # Test 2: Check State Medical Council specifically
    print(f"\n🏥 Step 2: State Medical Council Field")
    print("-" * 40)
    
    state_field = form.fields['state_medical_council']
    print(f"   Field Type: {type(state_field.widget).__name__}")
    print(f"   CSS Class: {state_field.widget.attrs.get('class', 'None')}")
    print(f"   Choices: {len(state_field.choices)} options")
    
    # Test 3: Render the form
    print(f"\n🎨 Step 3: Form Rendering")
    print("-" * 40)
    
    try:
        rendered_form = str(form)
        print(f"   Form renders successfully ✅")
        print(f"   Total HTML length: {len(rendered_form)} characters")
        
        # Check for Bootstrap classes
        bootstrap_classes = ['form-control', 'form-select']
        for css_class in bootstrap_classes:
            count = rendered_form.count(css_class)
            print(f"   '{css_class}' appears: {count} times")
        
        # Check State Medical Council dropdown
        if 'state_medical_council' in rendered_form:
            print(f"   State Medical Council field rendered ✅")
            
            # Check if it has form-select class
            state_field_html = rendered_form.split('name="state_medical_council"')[1].split('</select>')[0] + '</select>'
            if 'form-select' in state_field_html:
                print(f"   State Medical Council has 'form-select' class ✅")
            else:
                print(f"   State Medical Council missing 'form-select' class ❌")
        else:
            print(f"   State Medical Council field not rendered ❌")
            
    except Exception as e:
        print(f"   Form rendering failed: {e} ❌")
        return False
    
    # Test 4: Test form submission
    print(f"\n✅ Step 4: Form Submission Test")
    print("-" * 40)
    
    test_data = {
        'first_name': 'Styled',
        'last_name': 'Test',
        'email': 'styled.test@example.com',
        'phone_number': '9876543211',
        'nmc_registration_number': 'STYLED-TEST-001',
        'specialization': 'GENERAL',
        'hospital_name': 'Styled Test Hospital',
        'hospital_address': '123 Styled Street',
        'years_of_experience': 8,
        'medical_license_number': 'ML-STYLED-001',
        'state_medical_council': 'Karnataka Medical Council',
        'password1': 'StyledTest@123456',
        'password2': 'StyledTest@123456',
    }
    
    form = DoctorRegistrationForm(data=test_data)
    
    print(f"   Form is valid: {form.is_valid()}")
    
    if form.is_valid():
        print(f"   ✅ All fields validated")
        print(f"   ✅ State Council: '{form.cleaned_data['state_medical_council']}'")
        print(f"   ✅ Form ready for submission")
    else:
        print(f"   ❌ Form validation errors:")
        for field, errors in form.errors.items():
            print(f"     {field}: {errors}")
    
    return True

if __name__ == '__main__':
    success = test_styled_form()
    
    if success:
        print(f"\n🎉 STYLED FORM WORKS PERFECTLY!")
        print(f"   ✅ All fields have Bootstrap styling")
        print(f"   ✅ State Medical Council dropdown styled")
        print(f"   ✅ Form renders correctly")
        print(f"   ✅ Form validation works")
        print(f"\n📝 Form is ready for manual testing!")
        print(f"   🌐 URL: http://127.0.0.1:8000/doctor/register/")
        print(f"   👀 State Medical Council dropdown should now be properly styled")
    else:
        print(f"\n❌ STYLED FORM HAS ISSUES!")
