from channels.generic.websocket import AsyncWebsocketConsumer
import json
class Aiserver(AsyncWebsocketConsumer):
    async def connect(self):
        from doctors.ai import Psychologist
        self.suri = Psychologist()
        self.room_group_name = 'suri'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            if "issue" in message :
                if self.suri.issue == "" :
                    chat = "you seems ok"
                else :
                    chat = self.suri.issue
            elif "meditation" in message :
                chat =  self.suri.meditation_guide(self.suri.issue)
            elif "to commit suicide" in message :
                chat = "This is  serious ,  contact with this number now.... helpline number : 911 ; or contact with Dr. Nilanjana Mam Noww "
            else :
                chat =  self.suri.ask("user" , message)
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
        pass
