from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Message, MessageHistory
from .serializers import  MessageSerializer, MessageHistorySerializer
from ..chats.serializers import UserSerializer

@api_view(['DELETE'])
def delete_user(request):
    """Allow authenticated user to delete their account."""
    user = request.user
    if not user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    username = user.username
    user.delete()
    return Response({"detail": f"User {username} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict to messages where user is sender or receiver."""
        user = self.request.user
        return Message.objects.filter(
            sender=user
        ) | Message.objects.filter(
            receiver=user
        )

    def perform_update(self, serializer):
        """Set edited_by to current user on update."""
        serializer.save(edited_by=self.request.user)

class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict history to messages where user is sender or receiver."""
        user = self.request.user
        return MessageHistory.objects.filter(
            message__sender=user
        ) | MessageHistory.objects.filter(
            message__receiver=user
        )