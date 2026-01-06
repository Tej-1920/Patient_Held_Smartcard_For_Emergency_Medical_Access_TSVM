from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.patient_login, name='login'),
    path('logout/', views.patient_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('upload-record/', views.upload_record, name='upload_record'),
    path('records/', views.view_records, name='view_records'),
    path('records/<uuid:record_id>/', views.view_record_detail, name='view_record_detail'),
    path('records/<uuid:record_id>/delete/', views.delete_record, name='delete_record'),
]
