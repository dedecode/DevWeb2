from rest_framework import serializers
from .models import DailySummary, WeeklySummary

class DailySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySummary
        fields = ['id', 'user', 'date', 'title', 'content']
        read_only_fields = ['user']

class WeeklySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySummary
        fields = ['id', 'user', 'week_start', 'week_end', 'title', 'content']
        read_only_fields = ['user']
