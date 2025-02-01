# authentication/accounts/management/commands/verify_users.py

from django.core.management.base import BaseCommand
from authentication.accounts.models import UserRegister

class Command(BaseCommand):
    help = 'Verify users in the database'

    def handle(self, *args, **kwargs):
        users = UserRegister.objects.all()
        if users.exists():
            for user in users:
                self.stdout.write(f"User: {user.username}, Email: {user.email}, Businessname: {user.businessname}, Phone: {user.phone}")
        else:
            self.stdout.write("No users found in the database.")