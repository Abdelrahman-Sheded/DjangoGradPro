from django.contrib import admin
from .models import User, ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'message_preview', 'timestamp')
    list_filter = ('sender', 'timestamp', 'user')
    search_fields = ('message', 'user__username')
    readonly_fields = ('timestamp',)

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

# Register the User model
admin.site.register(User)
