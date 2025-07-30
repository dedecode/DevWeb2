from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import DailySummary, WeeklySummary
from .serializers import DailySummarySerializer, WeeklySummarySerializer

class DailySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = DailySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailySummary.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current_week(self, request):
        """Retorna resumos da semana atual"""
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        summaries = self.get_queryset().filter(
            date__range=[start_of_week, end_of_week]
        )
        serializer = self.get_serializer(summaries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def last_week(self, request):
        """Retorna resumos da semana passada"""
        today = timezone.now().date()
        start_of_last_week = today - timedelta(days=today.weekday() + 7)
        end_of_last_week = start_of_last_week + timedelta(days=6)
        
        summaries = self.get_queryset().filter(
            date__range=[start_of_last_week, end_of_last_week]
        )
        serializer = self.get_serializer(summaries, many=True)
        return Response(serializer.data)

class WeeklySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = WeeklySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WeeklySummary.objects.filter(user=self.request.user).order_by('-week_start')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)