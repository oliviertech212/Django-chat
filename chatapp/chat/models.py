from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    chat_groups = models.ManyToManyField(
        'Group',  # Reference your custom Group model
        related_name='user_chat_groups',  # Changed to avoid conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="admin_groups"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="group_members",  # Changed to avoid conflict
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_or_create_conversation(self):
        conversation, created = Conversation.objects.get_or_create(group=self)
        return conversation

class Conversation(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True, related_name="conversations"
    )
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_participant"
    )
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group',)

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='message_sender'
    )
    text = models.TextField(blank=True)
    attachment = models.FileField(blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)


# from django.db import models
# from django.conf import settings


# # Create your models here.

# class Conversation(models.Model):
#     initiator = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
#     )
#     receiver = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_participant"
#     )
#     start_time = models.DateTimeField(auto_now_add=True)


# class Message(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
#                               null=True, related_name='message_sender')
#     text = models.CharField(max_length=200, blank=True)
#     attachment = models.FileField(blank=True)
#     conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE,)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('-timestamp',)
