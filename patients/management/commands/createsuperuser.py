from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from patients.models import Patient

class Command(BaseCommand):
    help = 'Create a superuser for the Patient Smart Card system'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Superuser email')
        parser.add_argument('--password', type=str, help='Superuser password')
        parser.add_argument('--first-name', type=str, help='Superuser first name')
        parser.add_argument('--last-name', type=str, help='Superuser last name')
        parser.add_argument('--phone', type=str, help='Superuser phone number')

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get user input if not provided via arguments
        email = options.get('email') or input('Email: ')
        password = options.get('password') or input('Password: ')
        first_name = options.get('first_name') or input('First name: ')
        last_name = options.get('last_name') or input('Last name: ')
        phone_number = options.get('phone') or input('Phone number: ')

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists.')
            )
            return

        # Create superuser
        try:
            user = User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Superuser {email} created successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
