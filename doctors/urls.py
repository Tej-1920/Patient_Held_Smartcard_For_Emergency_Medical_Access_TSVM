from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_validator_home, name='home'),
    path('register/', views.doctor_register, name='register'),
    path('login/', views.doctor_login, name='login'),
    path('logout/', views.doctor_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.doctor_profile, name='profile'),
    path('search-patient/', views.search_patient, name='search_patient'),
    path('emergency-access/', views.emergency_access, name='emergency_access'),
    path('patient/<uuid:patient_id>/', views.view_patient_profile, name='view_patient_profile'),
    path('patient/<uuid:patient_id>/records/', views.view_patient_records, name='view_patient_records'),
    path('access-logs/', views.access_logs, name='access_logs'),
]
