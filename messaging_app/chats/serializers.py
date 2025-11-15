"""
    Serializers for the messaging app, including User, Conversation, and Message serializers.
"""

from rest_framework import serializers

from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.

    Exposes safe fields only (not the raw password),
    and matches the main attributes from the spec.
    """

    class Meta:
        model = User
        # user_id is the primary key field on the model
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]
        extra_kwargs = {
            # password is handled specially by Django's auth system
            "password": {"write_only": True},
        }


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.

    Includes:
    - message_id
    - sender (nested user representation for reading)
    - conversation (id reference)
    - message_body
    - sent_at
    """

    sender = UserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        source="sender",
        queryset=User.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "sender_id",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["message_id", "sent_at"]

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.

    Includes:
    - conversation_id
    - participants (nested users)
    - messages (nested messages in this conversation)
    - created_at
    """

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]
