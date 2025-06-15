from django.contrib import admin
from .models import User, Message, Notification, MessageHistory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_id')
    search_fields = ('username', 'email')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'content', 'timestamp','edited', 'edited_by', 'parent_message','unread')
    search_fields = ('content',)
    list_filter = ('timestamp',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'message', 'old_content', 'edited_at')
    search_fields = ('old_content',)
    list_filter = ('edited_at',)