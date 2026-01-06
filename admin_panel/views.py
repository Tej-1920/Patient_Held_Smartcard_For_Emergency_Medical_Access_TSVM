from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from patients.models import Patient, MedicalRecord
from doctors.models import Doctor, AccessLog
from patients.utils import doctor_validator
from django.utils import timezone

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Changed from username to email
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # Use email as username
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, 'Admin login successful!')
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'admin_panel/login.html')

def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('admin_panel:login')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    verified_doctors = Doctor.objects.filter(is_verified=True).count()
    pending_doctors = Doctor.objects.filter(is_verified=False).count()
    
    recent_access_logs = AccessLog.objects.select_related('doctor', 'patient').order_by('-accessed_at')[:10]
    
    validation_stats = doctor_validator.get_statistics()
    
    return render(request, 'admin_panel/dashboard.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'verified_doctors': verified_doctors,
        'pending_doctors': pending_doctors,
        'recent_access_logs': recent_access_logs,
        'validation_stats': validation_stats
    })

@login_required
def manage_patients(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/manage_patients.html', {'patients': patients})

@login_required
def manage_doctors(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    doctors = Doctor.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/manage_doctors.html', {'doctors': doctors})

@login_required
def view_access_logs(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    logs = AccessLog.objects.all().order_by('-accessed_at')
    
    # Calculate statistics
    emergency_count = logs.filter(access_type='EMERGENCY').count()
    authorized_count = logs.filter(validation_status='AUTHORIZED').count()
    blacklisted_count = logs.filter(validation_status='BLACKLISTED').count()
    not_found_count = logs.filter(validation_status='NOT_FOUND').count()
    
    context = {
        'logs': logs,
        'emergency_count': emergency_count,
        'authorized_count': authorized_count,
        'blacklisted_count': blacklisted_count,
        'not_found_count': not_found_count,
    }
    
    return render(request, 'admin_panel/access_logs.html', context)

@login_required
def delete_patient(request, patient_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        patient_name = f"{patient.first_name} {patient.last_name}"
        patient.delete()
        messages.success(request, f'Patient {patient_name} has been deleted successfully.')
        return redirect('admin_panel:manage_patients')
    
    return render(request, 'admin_panel/delete_patient.html', {'patient': patient})

@login_required
def delete_doctor(request, doctor_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        doctor_name = f"{doctor.first_name} {doctor.last_name}"
        doctor.delete()
        messages.success(request, f'Doctor {doctor_name} has been deleted successfully.')
        return redirect('admin_panel:manage_doctors')
    
    return render(request, 'admin_panel/delete_doctor.html', {'doctor': doctor})

@login_required
def verify_doctor(request, doctor_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        doctor.is_verified = True
        doctor.verification_date = timezone.now()
        doctor.save()
        messages.success(request, f'Dr. {doctor.first_name} {doctor.last_name} has been verified.')
        return redirect('admin_panel:manage_doctors')
    
    return render(request, 'admin_panel/verify_doctor.html', {'doctor': doctor})

@login_required
def view_patient_details(request, patient_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Get patient's medical records
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-uploaded_at')
    
    context = {
        'patient': patient,
        'medical_records': medical_records,
        'total_records': medical_records.count(),
    }
    
    return render(request, 'admin_panel/view_patient_details.html', context)

@login_required
def view_doctor_details(request, doctor_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_panel:login')
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Get doctor's access logs
    access_logs = AccessLog.objects.filter(doctor=doctor).order_by('-accessed_at')[:10]
    
    context = {
        'doctor': doctor,
        'access_logs': access_logs,
        'total_access_logs': AccessLog.objects.filter(doctor=doctor).count(),
    }
    
    return render(request, 'admin_panel/view_doctor_details.html', context)
