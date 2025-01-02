from .models import Conversation, Message, Group
from rest_framework import serializers

# Move the import of `UserSerializer` inside a function to delay the import
def get_user_serializer():
    from users.serializers import UserSerializer  # Import here to delay it
    return UserSerializer

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         exclude = ('conversation_id',)
class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.IntegerField(source='conversation.id', read_only=True)  # Adjust if needed

    class Meta:
        model = Message
        exclude = ('conversation',)  # Exclude conversation if needed

class ConversationListSerializer(serializers.ModelSerializer):
    # Use the delayed UserSerializer import
    initiator = get_user_serializer()
    receiver = get_user_serializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message).data

class ConversationSerializer(serializers.ModelSerializer):
    # Use the delayed UserSerializer import
    initiator = get_user_serializer()
    receiver = get_user_serializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['initiator', 'receiver', 'message_set']
