from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """Allow access only to participants of a conversation for specific methods."""
    def has_permission(self, request, view):
        """Ensure user is authenticated for all actions."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Restrict access to conversation participants for GET, POST, PUT, PATCH, DELETE."""
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if isinstance(obj, Conversation):
                return obj.participants.filter(user_id=request.user.user_id).exists()
            elif isinstance(obj, Message):
                return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        elif request.method in ['GET', 'POST']:
            if isinstance(obj, Conversation):
                return obj.participants.filter(user_id=request.user.user_id).exists()
            elif isinstance(obj, Message):
                return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        return False