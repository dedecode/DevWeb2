from rest_framework import viewsets, permissions
from .models import DailySummary, WeeklySummary
from .serializers import DailySummarySerializer, WeeklySummarySerializer
from rest_framework.permissions import IsAuthenticated

class DailySummaryViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar resumos diários do usuário autenticado.
    Permite criar, visualizar, atualizar e deletar resumos por data.
    """
    serializer_class = DailySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailySummary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WeeklySummaryViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar resumos semanais do usuário autenticado.
    Permite criar, visualizar, atualizar e deletar resumos por semana.
    """
    serializer_class = WeeklySummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WeeklySummary.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

