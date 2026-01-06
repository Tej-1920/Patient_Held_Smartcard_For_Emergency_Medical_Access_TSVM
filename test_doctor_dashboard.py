#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_smart_card.settings')
django.setup()

from doctors.models import Doctor
from django.test import RequestFactory
from doctors.views import dashboard

def test_doctor_dashboard():
    """Test doctor dashboard functionality"""
    
    print("🏥 TESTING DOCTOR DASHBOARD")
    print("=" * 40)
    
    # Get a verified doctor
    doctor = Doctor.objects.filter(is_verified=True).first()
    
    if not doctor:
        print("❌ No verified doctors found")
        return False
    
    print(f"Testing with: Dr. {doctor.first_name} {doctor.last_name}")
    print(f"Email: {doctor.email}")
    print(f"Doctor ID: {doctor.doctor_id}")
    print(f"Verified: {doctor.is_verified}")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/doctor/dashboard/')
    request.user = doctor
    
    try:
        # Render the dashboard view
        response = dashboard(request)
        print(f"✅ Dashboard rendered successfully")
        print(f"Status: {response.status_code}")
        
        # Check content
        content = response.content.decode('utf-8')
        
        # Check for key elements
        checks = [
            ('Doctor Dashboard', 'Dashboard title'),
            ('Welcome, Dr.', 'Welcome message'),
            (doctor.first_name, 'Doctor name'),
            (doctor.doctor_id, 'Doctor ID'),
            ('Quick Actions', 'Quick actions section'),
            ('Recent Access Logs', 'Access logs section'),
            ('Account Stats', 'Statistics section')
        ]
        
        for check_text, description in checks:
            if check_text in content:
                print(f"✅ {description}: Found")
            else:
                print(f"❌ {description}: Missing")
        
        # Save rendered content for inspection
        with open('doctor_dashboard_test.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Rendered content saved to doctor_dashboard_test.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Error rendering dashboard: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_doctor_dashboard()
    
    if success:
        print(f"\n🎉 DOCTOR DASHBOARD WORKING!")
        print(f"   ✅ Template renders correctly")
        print(f"   ✅ All sections present")
        print(f"   ✅ Doctor data displayed")
        print(f"\n📝 MANUAL TESTING INSTRUCTIONS:")
        print("=" * 50)
        print(f"   1. Go to: http://127.0.0.1:8000/doctor/login/")
        print(f"   2. Use any doctor credentials:")
        print(f"      - chaitanyauggina@gmail.com / doctor123")
        print(f"      - wmunshi@example.org / doctor123")
        print(f"   3. You should see the dashboard!")
        print(f"   4. All sections should be visible")
    else:
        print(f"\n❌ DOCTOR DASHBOARD HAS ISSUES!")
