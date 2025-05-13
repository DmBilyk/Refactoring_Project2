from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import UserAuthService

# Define constants for template paths
LOGIN_TEMPLATE = 'registration_app/login.html'
REGISTER_TEMPLATE = 'registration_app/register.html'


class LoginView(View):
    """View handling user login process."""

    def get(self, request):
        """Render login page for GET requests."""
        if request.user.is_authenticated:
            return redirect('index')

        form = AuthenticationForm()
        return render(request, LOGIN_TEMPLATE, {'form': form})

    def post(self, request):
        """Process login form submission."""
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = UserAuthService.authenticate_user(
                form.cleaned_data.get('username'),
                form.cleaned_data.get('password')
            )

            if user is None:
                messages.error(request, "Invalid username or password.")
                return render(request, LOGIN_TEMPLATE, {'form': form})

            login(request, user)
            return redirect(request.GET.get('next', 'index'))

        return render(request, LOGIN_TEMPLATE, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """View handling user logout process."""

    def get(self, request):
        """Process user logout."""
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('index')


class RegisterView(View):
    """View handling user registration process."""

    def get(self, request):
        """Render registration page."""
        form = UserAuthService.get_registration_form()
        return render(request, REGISTER_TEMPLATE, {'form': form})

    def post(self, request):
        """Process registration form submission."""
        form = UserAuthService.get_registration_form(request.POST)

        if form.is_valid():
            user = UserAuthService.register_user(form)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('index')

        return render(request, REGISTER_TEMPLATE, {'form': form})