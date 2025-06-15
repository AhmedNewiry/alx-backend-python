from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
import logging
from ..chats.models import User
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create a notification for the receiver when a new message is created."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log the old content of a message before it is updated."""
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                instance.edited = True
                instance.edited_by = instance.sender
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """Log user deletion and ensure related data is cleaned up."""
    logging.info(f"User {instance.username} (ID: {instance.user_id}) deleted.")
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
