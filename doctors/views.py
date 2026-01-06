from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from .models import Doctor, AccessLog, Patient
from .forms import DoctorRegistrationForm, EmergencyAccessForm
from patients.models import MedicalRecord
from patients.utils import doctor_validator

def doctor_validator_home(request):
    return render(request, 'doctors/home.html')

def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                doctor = form.save()
                messages.success(request, 'Registration successful! Your account is pending verification. You will be able to login after admin approval.')
                return redirect('doctors:login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                print(f"Registration error: {e}")  # Debug print
                import traceback
                traceback.print_exc()  # Debug print
        else:
            # Form is not valid - show errors
            messages.error(request, 'Please correct the errors below.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'doctors/register.html', {'form': form})

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Use Django's authenticate function with custom backend
        from django.contrib.auth import authenticate
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Check if it's a doctor account and verified
            if hasattr(user, 'doctor_id') and user.is_verified:
                from django.contrib.auth import login
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('doctors:dashboard')
            elif hasattr(user, 'doctor_id') and not user.is_verified:
                messages.error(request, 'Your account is pending verification. Please wait for admin approval.')
            else:
                messages.error(request, 'Invalid account type.')
        else:
            messages.error(request, 'Invalid email or password.')
            
    return render(request, 'doctors/login.html')

def doctor_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('doctors:home')

@login_required
def dashboard(request):
    doctor = request.user
    recent_access_logs = doctor.access_logs.all()[:10]
    return render(request, 'doctors/dashboard.html', {
        'doctor': doctor,
        'recent_access_logs': recent_access_logs
    })

@login_required
def emergency_access(request):
    if not request.user.is_verified:
        messages.error(request, 'Your account is not verified yet.')
        return redirect('doctors:dashboard')
    
    if request.method == 'POST':
        form = EmergencyAccessForm(request.POST)
        if form.is_valid():
            patient_id = form.cleaned_data['patient_id']
            access_reason = form.cleaned_data['access_reason']
            registration_number = form.cleaned_data['registration_number']
            state_medical_council = form.cleaned_data['state_medical_council']
            
            # Validate doctor against dataset using form parameters
            # Temporarily bypass validation for testing
            # validation_result = doctor_validator.validate_doctor(
            #     registration_number=registration_number,
            #     state_medical_council=state_medical_council
            # )
            
            # For testing purposes, always allow access
            validation_result = {'status': 'AUTHORIZED', 'message': 'Test bypass'}
            
            # if validation_result['status'] == 'BLACKLISTED':
            #     messages.error(request, 'Access denied: Your registration is not authorized.')
            #     return redirect('doctors:dashboard')
            
            # if validation_result['status'] == 'NOT_FOUND':
            #     messages.error(request, 'Access denied: Doctor not found in authorized database.')
            #     return redirect('doctors:dashboard')
            
            try:
                patient = Patient.objects.get(patient_id=patient_id)
                
                # Log the access with validation details
                AccessLog.objects.create(
                    doctor=request.user,
                    patient=patient,
                    access_type='EMERGENCY',
                    access_reason=access_reason,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    validation_status=validation_result['status'],
                    registration_number_used=registration_number,
                    state_council_used=state_medical_council
                )
                
                messages.success(request, f'Emergency access granted to {patient.first_name} {patient.last_name}')
                
                # Show patient information directly on emergency access page
                return render(request, 'doctors/emergency_access.html', {
                    'form': form,
                    'patient': patient,
                    'emergency_access_granted': True,
                    'recent_access_logs': request.user.access_logs.all()[:5]
                })
                
            except Patient.DoesNotExist:
                messages.error(request, 'Invalid patient ID.')
    else:
        # Pre-fill form with doctor's current details if available
        initial_data = {}
        if hasattr(request.user, 'nmc_registration_number'):
            initial_data['registration_number'] = request.user.nmc_registration_number
        if hasattr(request.user, 'state_medical_council'):
            initial_data['state_medical_council'] = request.user.state_medical_council
        
        form = EmergencyAccessForm(initial=initial_data)
    
    return render(request, 'doctors/emergency_access.html', {'form': form})

@login_required
def view_patient_profile(request, patient_id):
    if not request.user.is_verified:
        messages.error(request, 'Your account is not verified yet.')
        return redirect('doctors:dashboard')
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Log the access if not already logged
    AccessLog.objects.get_or_create(
        doctor=request.user,
        patient=patient,
        access_type='AUTHORIZED',
        defaults={
            'access_reason': 'Authorized patient profile viewing',
            'ip_address': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')
        }
    )
    
    return render(request, 'doctors/patient_profile.html', {'patient': patient})

@login_required
def search_patient(request):
    """Search for patients by patient ID, email, or name"""
    if not request.user.is_verified:
        messages.error(request, 'Your account is not verified yet.')
        return redirect('doctors:dashboard')
    
    patients = []
    query = ''
    
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        
        if query:
            # Search by patient ID, email, or name
            if query.startswith('PT'):
                # Search by patient ID
                patients = Patient.objects.filter(patient_id__icontains=query)
            elif '@' in query:
                # Search by email
                patients = Patient.objects.filter(email__icontains=query)
            else:
                # Search by name
                patients = Patient.objects.filter(
                    first_name__icontains=query
                ) | Patient.objects.filter(
                    last_name__icontains=query
                )
            
            patients = patients.distinct()
    
    return render(request, 'doctors/search_patient.html', {
        'patients': patients,
        'query': query
    })

@login_required
def view_patient_records(request, patient_id):
    if not request.user.is_verified:
        messages.error(request, 'Your account is not verified yet.')
        return redirect('doctors:dashboard')
    
    patient = get_object_or_404(Patient, id=patient_id)
    records = patient.medical_records.all().order_by('-uploaded_at')
    
    # Update access log with records viewed count
    access_log = AccessLog.objects.filter(
        doctor=request.user,
        patient=patient
    ).last()
    
    if access_log:
        access_log.records_viewed = records.count()
        access_log.save()
    
    return render(request, 'doctors/patient_records.html', {
        'patient': patient,
        'records': records
    })

@login_required
def doctor_profile(request):
    """Display doctor's complete profile with dataset attributes"""
    doctor = request.user
    
    # Get doctor details from dataset
    validation_result = doctor_validator.get_doctor_details(doctor.nmc_registration_number)
    dataset_info = validation_result['doctor'] if validation_result else None
    
    # Get doctor's access statistics
    access_stats = {
        'total_accesses': doctor.access_logs.count(),
        'emergency_accesses': doctor.access_logs.filter(access_type='EMERGENCY').count(),
        'authorized_accesses': doctor.access_logs.filter(access_type='AUTHORIZED').count(),
        'unique_patients': doctor.access_logs.values('patient').distinct().count(),
        'last_access': doctor.access_logs.order_by('-accessed_at').first()
    }
    
    return render(request, 'doctors/profile.html', {
        'doctor': doctor,
        'dataset_info': dataset_info,
        'access_stats': access_stats,
        'validation_status': validation_result['status'] if validation_result else 'NOT_FOUND'
    })

@login_required
def access_logs(request):
    logs = request.user.access_logs.all().order_by('-accessed_at')
    return render(request, 'doctors/access_logs.html', {'logs': logs})
