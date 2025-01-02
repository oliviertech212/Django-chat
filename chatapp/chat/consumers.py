
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Get the user from the scope
        self.user = self.scope["user"]

        # Check if the user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return
        print(self.user)

        # Check if the group exists and if the user is a member
        self.group = await self.get_group(self.room_name)
        
        if not self.group:
            # If group doesn't exist, close the connection
            await self.close()
            return
        
        # Check if the user is a member of the group
        if not await self.is_user_in_group(self.user, self.group):
            await self.close()
            return

        # Add the user to the channel layer group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # Fetch and send previous messages in the group
        previous_messages = await self.get_previous_messages(self.group)
        await self.send(text_data=json.dumps({
            'messages': previous_messages
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_message(self.user, self.group, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def get_group(self, room_name):
        from .models import Group
        
        try:
            return Group.objects.get(name=room_name)
        except Group.DoesNotExist:
            return None

    @database_sync_to_async
    def get_previous_messages(self, group):
        from .models import Message
        from .serializers import MessageSerializer
        
        messages = Message.objects.filter(conversation__group=group).order_by('-timestamp')
        return MessageSerializer(messages, many=True).data

    @database_sync_to_async
    def save_message(self, user, group, message):
        from .models import Message
        
        conversation = group.get_or_create_conversation()
        Message.objects.create(sender=user, text=message, conversation=conversation)

    @database_sync_to_async
    def is_user_in_group(self, user, group):
        # Assuming your Group model has a ManyToManyField to users named 'members'
        return group.members.filter(id=user.id).exists()



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async

# from chat.models import Group

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#      self.room_name = self.scope['url_route']['kwargs']['room_name']
#      self.room_group_name = f'chat_{self.room_name}'

#      self.user = self.scope["user"]

#      if not self.user.is_authenticated:
#         await self.close()
#         return

#      try:
#         self.group = await database_sync_to_async(Group.objects.prefetch_related('members').get)(name=self.room_name)
#      except Group.DoesNotExist:
#         await self.close()
#         return

#      if self.user not in self.group.members.all():
#         await self.close()
#         return

#      await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#      await self.accept()

#      # Fetch messages for the group
#     #  previous_messages = await self.get_previous_messages(self.group)
#     #  await self.send(text_data=json.dumps({'messages': previous_messages}))

#     # async def connect(self):
#     #     print(f"Connecting to room number: {self.scope['url_route']}")
#     #     self.room_name = self.scope['url_route']['kwargs']['room_name']
#     #     self.room_group_name = f'chat_{self.room_name}'

#     #     # Join room group
#     #     await self.channel_layer.group_add(
#     #         self.room_group_name,
#     #         self.channel_name
#     #     )

#     #     await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))