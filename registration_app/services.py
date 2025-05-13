from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class UserAuthService:
    """Service class for handling user authentication and registration."""

    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate a user with given credentials.


        """
        return authenticate(username=username, password=password)

    @staticmethod
    def get_registration_form(data=None):
        """
        Get registration form, optionally with POST data.


        """
        from .forms import RegistrationForm
        return RegistrationForm(data) if data else RegistrationForm()

    @staticmethod
    def register_user(form):
        """
        Register a new user from a valid registration form.


        """
        return form.save()