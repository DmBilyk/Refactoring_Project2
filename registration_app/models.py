from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta


class ConfirmationToken(models.Model):
    """Confirmation token for user registration."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Override save method to set expiration date."""
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(hours=24)
        return super().save(*args, **kwargs)

    def is_valid(self):
        """Check if the token is valid."""
        return not self.is_used and timezone.now() < self.expires_at

    def __str__(self):
        """String representation of the token."""
        return f"Token for {self.user.username}"