from django.db import models

# Create your models here.

from django.db import models
from django.utils.timezone import now


class URL(models.Model):
    original_url = models.URLField()  # The full original URL
    short_url = models.CharField(max_length=10, unique=True)  # Shortened identifier
    creation_timestamp = models.DateTimeField(auto_now_add=True)  # When it was created
    expiration_timestamp = models.DateTimeField()  # When the link will expire

    def is_expired(self):
        """Check if the URL has expired."""
        return now() > self.expiration_timestamp

    class Meta:
        db_table = 'url_info'


class Analytics(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name="analytics")  # Relates to the URL model
    access_timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'analytics'
