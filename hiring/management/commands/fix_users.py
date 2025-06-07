from django.core.management.base import BaseCommand
from hiring.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Fix user passwords and permissions'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            # Fix password if not hashed
            if not user.password.startswith('pbkdf2_sha256$'):
                user.password = make_password(user.password)
            
            # Set proper permissions
            if user.is_admin:
                user.is_staff = True
                user.is_superuser = True
            user.is_active = True
            
            # Save user
            user.save()
            
            # Create or update token
            Token.objects.get_or_create(user=user)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully fixed user: {user.username}')
            ) 