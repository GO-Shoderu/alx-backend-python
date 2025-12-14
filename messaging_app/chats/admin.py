from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message


# Register custom user model with admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Use Django’s built-in UserAdmin but adapt it to your custom fields
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)

    # Tell Django which field is used for identification (your PK is user_id)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone_number")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_active", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )


# Register conversation and messages (optional)
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "sender", "conversation", "sent_at")
    search_fields = ("message_body", "sender__username")
