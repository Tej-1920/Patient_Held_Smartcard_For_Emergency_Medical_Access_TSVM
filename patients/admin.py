from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Patient, MedicalRecord

@admin.register(Patient)
class PatientAdmin(UserAdmin):
    list_display = ('patient_id', 'email', 'first_name', 'last_name', 'phone_number', 'blood_group', 'created_at')
    list_filter = ('blood_group', 'gender', 'created_at')
    search_fields = ('patient_id', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)  # Fix: use tuple
    
    fieldsets = (
        (None, {'fields': ('patient_id', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'gender')}),
        ('Medical Information', {'fields': ('blood_group', 'chronic_diseases', 'allergies')}),
        ('Emergency Contact', {'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')}),
        ('Address', {'fields': ('address',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('patient_id', 'created_at', 'updated_at')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
    )

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'record_type', 'hospital_name', 'uploaded_at')
    list_filter = ('record_type', 'uploaded_at', 'hospital_name')
    search_fields = ('title', 'patient__first_name', 'patient__last_name', 'patient__patient_id', 'hospital_name')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        (None, {'fields': ('patient', 'record_type', 'title')}),
        ('Details', {'fields': ('description', 'file')}),
        ('Hospital Information', {'fields': ('hospital_name', 'doctor_name', 'date_of_record')}),
        ('Metadata', {'fields': ('uploaded_at',)}),
    )
    
    readonly_fields = ('uploaded_at',)
