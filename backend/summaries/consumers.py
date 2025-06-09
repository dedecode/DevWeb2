from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SummaryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("resumos", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("resumos", self.channel_name)

    async def receive(self, text_data):
        pass  # você pode adicionar algo aqui depois, se quiser

    async def send_summary_update(self, event):
        await self.send(text_data=json.dumps(event["content"]))
