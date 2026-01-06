import csv
import os
from django.conf import settings

class DoctorValidationService:
    """
    Service to validate doctors against active and blacklisted datasets
    """
    
    def __init__(self):
        self.active_doctors = []
        self.blacklisted_doctors = []
        self.load_datasets()
    
    def load_datasets(self):
        """Load doctor datasets from CSV files"""
        try:
            # Load active doctors
            active_file_path = os.path.join(settings.STATIC_ROOT, 'css', 'active_doctors_clean.csv')
            if not os.path.exists(active_file_path):
                active_file_path = os.path.join(settings.BASE_DIR, 'static', 'css', 'active_doctors_clean.csv')
            
            if os.path.exists(active_file_path):
                with open(active_file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.active_doctors = list(reader)
            
            # Load blacklisted doctors
            blacklisted_file_path = os.path.join(settings.STATIC_ROOT, 'css', 'blacklisted_doctors_clean.csv')
            if not os.path.exists(blacklisted_file_path):
                blacklisted_file_path = os.path.join(settings.BASE_DIR, 'static', 'css', 'blacklisted_doctors_clean.csv')
            
            if os.path.exists(blacklisted_file_path):
                with open(blacklisted_file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    self.blacklisted_doctors = list(reader)
                    
        except Exception as e:
            print(f"Error loading doctor datasets: {e}")
    
    def validate_doctor(self, registration_number=None, state_medical_council=None):
        """
        Validate if a doctor is authorized to access patient records
        
        Args:
            registration_number: Doctor's NMC registration number
            state_medical_council: Doctor's state medical council
            
        Returns:
            dict: Validation result with status and doctor details
        """
        # Check if doctor is blacklisted
        blacklisted = self._check_blacklist(registration_number, state_medical_council)
        if blacklisted:
            return {
                'status': 'BLACKLISTED',
                'message': 'Doctor is not authorized to access patient records',
                'doctor': blacklisted
            }
        
        # Check if doctor is in active list
        active = self._check_active(registration_number, state_medical_council)
        if active:
            return {
                'status': 'AUTHORIZED',
                'message': 'Doctor is authorized to access patient records',
                'doctor': active
            }
        
        return {
            'status': 'NOT_FOUND',
            'message': 'Doctor not found in authorized database',
            'doctor': None
        }
    
    def _check_blacklist(self, registration_number=None, state_medical_council=None):
        """Check if doctor is in blacklist"""
        for doctor in self.blacklisted_doctors:
            if registration_number and doctor.get('registration_number') == registration_number:
                return doctor
            if state_medical_council and doctor.get('state_medical_council') == state_medical_council:
                return doctor
        return None
    
    def _check_active(self, registration_number=None, state_medical_council=None):
        """Check if doctor is in active list"""
        for doctor in self.active_doctors:
            if registration_number and doctor.get('registration_number') == registration_number:
                return doctor
            if state_medical_council and doctor.get('state_medical_council') == state_medical_council:
                return doctor
        return None
    
    def get_doctor_details(self, registration_number):
        """Get detailed information about a doctor"""
        # First check active doctors
        for doctor in self.active_doctors:
            if doctor.get('registration_number') == registration_number:
                return {
                    'status': 'ACTIVE',
                    'doctor': doctor
                }
        
        # Then check blacklisted doctors
        for doctor in self.blacklisted_doctors:
            if doctor.get('registration_number') == registration_number:
                return {
                    'status': 'BLACKLISTED',
                    'doctor': doctor
                }
        
        return None
    
    def get_statistics(self):
        """Get statistics about the doctor database"""
        return {
            'total_active_doctors': len(self.active_doctors),
            'total_blacklisted_doctors': len(self.blacklisted_doctors),
            'state_councils_active': list(set(doc.get('state_medical_council') for doc in self.active_doctors if doc.get('state_medical_council'))),
            'qualifications_active': list(set(doc.get('qualification_1') for doc in self.active_doctors if doc.get('qualification_1')))
        }

# Global instance
doctor_validator = DoctorValidationService()
