from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return conversations where the authenticated user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Add the authenticated user as a participant when creating a conversation."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return messages from conversations where the authenticated user is a participant."""
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """Set the authenticated user as the sender when creating a message."""
        serializer.save(sender=self.request.user)