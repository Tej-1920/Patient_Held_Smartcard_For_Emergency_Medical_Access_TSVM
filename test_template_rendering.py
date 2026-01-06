#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from patients.models import Patient
from django.test import RequestFactory
from patients.views import dashboard

def test_template_rendering():
    """Test template rendering with actual patient data"""
    
    print("🎨 TESTING TEMPLATE RENDERING")
    print("=" * 40)
    
    # Get a patient with image
    patient_with_image = Patient.objects.filter(profile_image__isnull=False).first()
    
    if not patient_with_image:
        print("❌ No patient with image found")
        return False
    
    print(f"Testing with: {patient_with_image.first_name} {patient_with_image.last_name}")
    print(f"Image: {patient_with_image.profile_image}")
    print(f"Image URL: {patient_with_image.profile_image.url}")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    request.user = patient_with_image
    
    try:
        # Render the view
        response = dashboard(request)
        print(f"✅ View rendered successfully")
        print(f"Status: {response.status_code}")
        
        # Check content
        content = response.content.decode('utf-8')
        
        # Check for image URL in content
        if patient_with_image.profile_image.url in content:
            print(f"✅ Image URL found in template")
        else:
            print(f"❌ Image URL NOT found in template")
            
        # Check for conditional logic
        if 'patient.profile_image' in content:
            print(f"✅ Template logic present")
        else:
            print(f"❌ Template logic missing")
            
        # Check for actual image tag
        if '<img src=' in content:
            print(f"✅ Image tag present")
        else:
            print(f"❌ Image tag missing")
            
        # Save rendered content for inspection
        with open('debug_dashboard.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Rendered content saved to debug_dashboard.html")
        
        # Show relevant parts
        print(f"\n📄 Relevant Template Sections:")
        print("-" * 40)
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'profile_image' in line.lower() or 'patient profile' in line.lower():
                print(f"Line {i+1}: {line.strip()}")
                
    except Exception as e:
        print(f"❌ Error rendering template: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    test_template_rendering()
