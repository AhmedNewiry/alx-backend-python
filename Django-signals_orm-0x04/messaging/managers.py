from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """Filter unread messages for a specific user."""
        return self.get_queryset().filter(receiver=user, unread=True)