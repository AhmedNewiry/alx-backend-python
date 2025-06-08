from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        """Return conversations where the authenticated user is a participant."""
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Add the authenticated user as a participant when creating a conversation."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        """Return messages from conversations where the authenticated user is a participant."""
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """Set the authenticated user as the sender when creating a message."""
        message = serializer.save(sender=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)