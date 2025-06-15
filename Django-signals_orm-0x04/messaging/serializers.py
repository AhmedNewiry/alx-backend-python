from rest_framework import serializers
from .models import User, Message, Notification, MessageHistory


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    edited_by = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'edited_by']

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ['notification_id', 'user', 'message', 'created_at', 'is_read']

class MessageHistorySerializer(serializers.ModelSerializer):
    message = MessageSerializer(read_only=True)
    class Meta:
        model = MessageHistory
        fields = ['history_id', 'message', 'old_content', 'edited_at']