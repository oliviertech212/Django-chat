# from django.shortcuts import render
# from .models import Conversation
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from users.models import MyUser as User
# from .serializers import ConversationListSerializer, ConversationSerializer
# from django.db.models import Q
# from django.shortcuts import redirect, reverse


# from django.shortcuts import render, get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Group, Conversation, Message
# from users.models import MyUser as User
# from .serializers import (
#     GroupSerializer, ConversationSerializer, MessageSerializer
# )
# from django.db.models import Q



# @api_view(['POST'])
# def create_group(request):
#     if not request.user.is_authenticated:
#         return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

#     data = request.data
#     group_name = data.get('name')
#     if Group.objects.filter(name=group_name).exists():
#         return Response({'message': 'Group with this name already exists.'}, status=400)

#     group = Group.objects.create(name=group_name, admin=request.user)
#     group.members.add(request.user)
#     return Response({'message': 'Group created successfully!'})

# # //get all groups
# @api_view(['GET'])
# def get_groups(request):
#     if not request.user.is_authenticated:
#         return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

#     groups = Group.objects.filter(members=request.user)
#     return Response(GroupSerializer(groups, many=True).data)

# # user chat with another user privately 




# @api_view(['POST'])
# def join_group(request, group_id):
#     if not request.user.is_authenticated:
#         return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

#     group = get_object_or_404(Group, id=group_id)
#     group.members.add(request.user)
#     return Response({'message': f'{request.user.username} joined the group {group.name}.'})

# @api_view(['POST'])
# def send_message_to_group(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     if request.user not in group.members.all():
#         return Response({'message': 'You are not a member of this group.'}, status=403)

#     data = request.data
#     message = Message.objects.create(
#         sender=request.user,
#         text=data.get('message', ''),
#         conversation=group.conversations.first()  # Assuming one conversation per group
#     )
#     return Response({'message': 'Message sent successfully!'})

# @api_view(['GET'])
# def group_messages(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     if request.user not in group.members.all():
#         return Response({'message': 'You are not a member of this group.'}, status=403)

#     messages = Message.objects.filter(conversation__group=group).order_by('-timestamp')
#     return Response(MessageSerializer(messages, many=True).data)



from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Group, Conversation, Message
from users.models import MyUser as User
from .serializers import GroupSerializer, MessageSerializer

from django.db.models import Q

@api_view(['POST'])
def create_group(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    data = request.data
    group_name = data.get('name')
    if Group.objects.filter(name=group_name).exists():
        return Response({'message': 'Group with this name already exists.'}, status=400)

    group = Group.objects.create(name=group_name, admin=request.user)
    group.members.add(request.user)
    return Response({'message': 'Group created successfully!'})

# @api_view(['GET'])
# def get_groups(request):
#     if not request.user.is_authenticated:
#         return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

#     groups = Group.objects.filter(members=request.user)
#     return Response(GroupSerializer(groups, many=True).data)

@api_view(['POST'])
def join_group(request, group_id):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)
    return Response({'message': f'{request.user.username} joined the group {group.name}.'})

@api_view(['POST'])
def send_message_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        return Response({'message': 'You are not a member of this group.'}, status=403)

    data = request.data
    conversation = group.get_or_create_conversation()
    message = Message.objects.create(
        sender=request.user,
        text=data.get('message', ''),
        conversation=conversation
    )
    return Response({'message': 'Message sent successfully!'})
@api_view(['GET'])
def get_groups(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    groups = Group.objects.filter(members=request.user).prefetch_related('members')
    return Response(GroupSerializer(groups, many=True).data)

@api_view(['GET'])
def group_messages(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.user not in group.members.all():
        return Response({'message': 'You are not a member of this group.'}, status=403)

    messages = Message.objects.filter(conversation__group=group).select_related('sender').order_by('-timestamp')
    return Response(MessageSerializer(messages, many=True).data)


# @api_view(['GET'])
# def group_messages(request, group_id):
#     group = get_object_or_404(Group, id=group_id)
#     if request.user not in group.members.all():
#         return Response({'message': 'You are not a member of this group.'}, status=403)

#     messages = Message.objects.filter(conversation__group=group).order_by('-timestamp')
#     return Response(MessageSerializer(messages, many=True).data)


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })