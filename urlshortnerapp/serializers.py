from django.db.migrations import serializer
from rest_framework import serializers

from urlshortnerapp.models import URL, Analytics


class ShortenURLSerializer(serializers.ModelSerializer):

    class Meta:
        model=URL
        fields='__all__'



class AnalyticsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Analytics
        fields='__all__'