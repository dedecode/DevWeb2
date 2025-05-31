from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DailySummary, WeeklySummary
from .serializers import DailySummarySerializer, WeeklySummarySerializer

class DailySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = DailySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailySummary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WeeklySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = WeeklySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WeeklySummary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
