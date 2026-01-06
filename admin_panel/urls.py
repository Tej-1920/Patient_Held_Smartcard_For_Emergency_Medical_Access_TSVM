from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('patients/', views.manage_patients, name='manage_patients'),
    path('patients/<uuid:patient_id>/', views.view_patient_details, name='view_patient_details'),
    path('patients/delete/<uuid:patient_id>/', views.delete_patient, name='delete_patient'),
    path('doctors/', views.manage_doctors, name='manage_doctors'),
    path('doctors/<uuid:doctor_id>/', views.view_doctor_details, name='view_doctor_details'),
    path('doctors/delete/<uuid:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('access-logs/', views.view_access_logs, name='view_access_logs'),
    path('verify-doctor/<uuid:doctor_id>/', views.verify_doctor, name='verify_doctor'),
]
