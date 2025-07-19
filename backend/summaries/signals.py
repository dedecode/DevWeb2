from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import DailySummary, WeeklySummary

# Esta função será executada automaticamente sempre que um
# DailySummary ou WeeklySummary for salvo no banco.
@receiver(post_save, sender=DailySummary)
@receiver(post_save, sender=WeeklySummary)
def summary_saved_handler(sender, instance, created, **kwargs):
    """
    Dispara um evento para o grupo 'summaries' via WebSocket
    após um resumo ser salvo.
    """
    channel_layer = get_channel_layer()
    group_name = "summaries"  # Nome do grupo (em inglês, como sugerido)

    action = "criado" if created else "atualizado"
    message = f"Resumo '{instance.title}' foi {action}."

    # Prepara o pacote de dados para enviar ao frontend
    event = {
        "type": "summary_notification",  # IMPORTANTE: nome do método no consumer
        "content": {
            "message": message,
            "summary_id": instance.id,
            "title": instance.title,
            "user": instance.user.username
        }
    }

    # Envia o evento para todos os clientes conectados ao grupo 'summaries'
    async_to_sync(channel_layer.group_send)(group_name, event)