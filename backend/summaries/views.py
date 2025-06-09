from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DailySummary, WeeklySummary
from .serializers import DailySummarySerializer, WeeklySummarySerializer
from core.utils.pubsub import publish_event

class DailySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = DailySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailySummary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        publish_event("summary_channel", {
            "type": "daily",
            "id": instance.id,
            "title": instance.title,
            "created_by": self.request.user.username
        })

    def perform_update(self, serializer):
        instance = serializer.save()
        publish_event("summary_channel", {
            "type": "daily",
            "id": instance.id,
            "title": instance.title,
            "edited_by": self.request.user.username
        })

class WeeklySummaryViewSet(viewsets.ModelViewSet):
    serializer_class = WeeklySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WeeklySummary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        publish_event("summary_channel", {
            "type": "weekly",
            "id": instance.id,
            "title": instance.title,
            "created_by": self.request.user.username
        })

    def perform_update(self, serializer):
        instance = serializer.save()
        publish_event("summary_channel", {
            "type": "weekly",
            "id": instance.id,
            "title": instance.title,
            "edited_by": self.request.user.username
        })
