from rest_framework import serializers
from .models import Expert

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ['id', 'name', 'contact', 'region', 'district']
