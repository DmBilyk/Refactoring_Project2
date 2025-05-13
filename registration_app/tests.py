from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from django.contrib.auth import get_user_model


class AuthViewsTest(TestCase):

    def setUp(self):
        self.login_url = reverse('registration_app:login')
        self.logout_url = reverse('registration_app:logout')
        self.register_url = reverse('registration_app:register')
        self.index_url = reverse('index')
        self.credentials = {
            'username': 'testuser',
            'password': 'securepass123'
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_app/login.html')

    def test_login_post_valid(self):
        response = self.client.post(self.login_url, self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, self.index_url)

    def test_login_post_invalid(self):
        response = self.client.post(self.login_url, {
            'username': 'wrong',
            'password': 'incorrect'
        })
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'registration_app/login.html')

    def test_logout_get(self):
        login_successful = self.client.login(**self.credentials)
        self.assertTrue(login_successful)

        response = self.client.get(self.logout_url, follow=True)

        self.assertFalse(response.context['user'].is_authenticated)


        final_url = response.redirect_chain[-1][0]
        self.assertIn(self.index_url, final_url)

    @patch('registration_app.services.UserAuthService.get_registration_form')
    def test_register_get(self, mock_get_form):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_app/register.html')
        mock_get_form.assert_called_once()

    @patch('registration_app.services.UserAuthService.register_user')
    @patch('registration_app.services.UserAuthService.get_registration_form')
    def test_register_post_valid(self, mock_get_form, mock_register_user):
        mock_form = mock_get_form.return_value
        mock_form.is_valid.return_value = True

        user = get_user_model().objects.create_user(username='newuser', password='newpass123')
        mock_register_user.return_value = user

        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, follow=True)

        self.assertRedirects(response, self.index_url)
        self.assertTrue(response.context['user'].is_authenticated)
        mock_register_user.assert_called_once()

    @patch('registration_app.services.UserAuthService.get_registration_form')
    def test_register_post_invalid(self, mock_get_form):
        mock_form = mock_get_form.return_value
        mock_form.is_valid.return_value = False

        response = self.client.post(self.register_url, {
            'username': 'baduser',
            'password1': 'short',
            'password2': 'mismatch'
        })

        self.assertTemplateUsed(response, 'registration_app/register.html')
        mock_get_form.assert_called_once()
