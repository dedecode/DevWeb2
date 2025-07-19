import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SummaryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "summaries"

        # Conecta o cliente ao grupo 'summaries'
        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Desconecta o cliente do grupo
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    # Este método é chamado pelo `channel_layer.group_send`
    # quando o evento tem "type": "summary_notification"
    async def summary_notification(self, event):
        # Pega o dicionário 'content' que o sinal enviou
        content_data = event["content"]

        # Envia os dados para o cliente no frontend
        await self.send(text_data=json.dumps(content_data))