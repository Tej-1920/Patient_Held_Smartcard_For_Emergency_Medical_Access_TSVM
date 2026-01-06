from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, AccessLog

@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = ('doctor_id', 'email', 'first_name', 'last_name', 'specialization', 'is_verified', 'created_at')
    list_filter = ('specialization', 'is_verified', 'created_at')
    search_fields = ('doctor_id', 'email', 'first_name', 'last_name', 'nmc_registration_number', 'hospital_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('doctor_id', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Professional Information', {'fields': ('nmc_registration_number', 'medical_license_number', 'specialization', 'years_of_experience')}),
        ('Hospital Information', {'fields': ('hospital_name', 'hospital_address')}),
        ('Verification', {'fields': ('is_verified', 'verification_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('doctor_id', 'created_at', 'updated_at')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'nmc_registration_number', 'password1', 'password2'),
        }),
    )

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'access_type', 'accessed_at', 'ip_address', 'records_viewed')
    list_filter = ('access_type', 'accessed_at')
    search_fields = ('doctor__first_name', 'doctor__last_name', 'patient__first_name', 'patient__last_name', 'patient__patient_id')
    ordering = ('-accessed_at',)
    
    fieldsets = (
        (None, {'fields': ('doctor', 'patient', 'access_type')}),
        ('Access Details', {'fields': ('access_reason', 'records_viewed')}),
        ('Technical Information', {'fields': ('ip_address', 'user_agent', 'session_duration')}),
        ('Timestamp', {'fields': ('accessed_at',)}),
    )
    
    readonly_fields = ('accessed_at',)
