from channels.generic.websocket import AsyncWebsocketConsumer
import json
class Aiserver(AsyncWebsocketConsumer):
    async def connect(self):

        from doctors.ai import Psychologist
        if self.scope['user'] is not None:
            ids = self.scope['user']['id']
            username = self.scope['user']['username']

            self.room_group_name = f'SURI_{username}_{ids}'
        else :
            await self.close()

        self.suri = Psychologist(self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            if "meditation" in message :
                chat =  self.suri.meditation_guide(self.suri.issue)
            else :
                chat =  self.suri.ask(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data= json.dumps({
            'type': 'ai send',
            'text': message
        }))

    async def disconnect(self, close_code):
        self.suri.Delete_user_data()
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )