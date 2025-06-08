from rest_framework import serializers
from .models import User, Conversation, Message
import re

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15, allow_blank=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'bio', 'full_name']
        read_only_fields = ['user_id', 'full_name']

    def get_full_name(self, obj):
        """Return the user's full name by combining first_name and last_name."""
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_phone_number(self, value):
        """Validate phone number format (e.g., +1234567890 or 1234567890)."""
        if value and not re.match(r'^\+?\d{9,15}$', value):
            raise serializers.ValidationError("Phone number must be 9-15 digits, optionally starting with '+'.") 
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    message_body = serializers.CharField(max_length=1000)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'sender']

    def validate_message_body(self, value):
        """Ensure message_body is not empty and within length limits."""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(value) > 1000:
            raise serializers.ValidationError("Message body cannot exceed 1000 characters.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'updated_at', 'participant_count']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at', 'participant_count']

    def get_participant_count(self, obj):
        """Return the number of participants in the conversation."""
        return obj.participants.count()