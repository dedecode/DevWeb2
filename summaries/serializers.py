from rest_framework import serializers
from .models import DailySummary, WeeklySummary

class DailySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySummary
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class WeeklySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySummary
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
