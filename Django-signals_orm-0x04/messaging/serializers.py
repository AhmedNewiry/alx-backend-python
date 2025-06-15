from rest_framework import serializers
from .models import User, Message, Notification, MessageHistory


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    edited_by = UserSerializer(read_only=True)
    parent_message = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), allow_null=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'edited_by', 'parent_message', 'replies', 'unread']

    def get_replies(self, obj):
        """Recursively serialize replies."""
        replies = obj.get_thread()
        return MessageSerializer(replies, many=True, context=self.context).data

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