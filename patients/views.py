from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Patient, MedicalRecord
from .forms import PatientRegistrationForm, PatientProfileForm, MedicalRecordForm

def home(request):
    return render(request, 'patients/home.html')

def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('patients:dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'patients/register.html', {'form': form})

def patient_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('patients:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'patients/login.html')

def patient_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('patients:home')

@login_required
def dashboard(request):
    patient = request.user
    recent_records = patient.medical_records.all()[:5]
    return render(request, 'patients/dashboard.html', {
        'patient': patient,
        'recent_records': recent_records
    })

@login_required
def profile(request):
    patient = request.user
    return render(request, 'patients/profile.html', {'patient': patient})

@login_required
def edit_profile(request):
    patient = request.user
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            # Save the form
            form.save()
            
            # Generate QR code after profile update
            patient.generate_qr_code()
            
            messages.success(request, 'Profile updated successfully! QR code generated.')
            return redirect('patients:profile')
    else:
        form = PatientProfileForm(instance=patient)
    return render(request, 'patients/edit_profile.html', {'form': form})

@login_required
def upload_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = request.user
            record.save()
            messages.success(request, 'Medical record uploaded successfully!')
            return redirect('patients:view_records')
    else:
        form = MedicalRecordForm()
    return render(request, 'patients/upload_record.html', {'form': form})

@login_required
def view_records(request):
    records = request.user.medical_records.all().order_by('-uploaded_at')
    return render(request, 'patients/view_records.html', {'records': records})

@login_required
def view_record_detail(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, patient=request.user)
    return render(request, 'patients/record_detail.html', {'record': record})

@login_required
def delete_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, patient=request.user)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted successfully!')
        return redirect('patients:view_records')
    return render(request, 'patients/delete_record.html', {'record': record})
