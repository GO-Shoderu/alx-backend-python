from django.shortcuts import render

"""
Viewsets for the messaging app.

Provides API endpoints for:
- Listing and creating conversations
- Listing and sending messages within conversations
"""

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.

    - list: show conversations that the authenticated user participates in
    - create: create a new conversation and attach participants
    """

    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only conversations where the current user is a participant.
        """
        user = self.request.user
        return (
            Conversation.objects.filter(participants=user)
            .prefetch_related("participants", "messages__sender")
            .order_by("-created_at")
        )

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.

        Expected payload:
        {
            "participants": ["<user_id_1>", "<user_id_2>", ...]
        }

        The authenticated user will automatically be included as a participant.
        """
        participant_ids = request.data.get("participants", [])

        if not isinstance(participant_ids, list):
            raise ValidationError({"participants": "This field must be a list of user IDs."})

        # Always include the current user
        participant_ids.append(str(request.user.user_id))
        # Remove duplicates
        participant_ids = list(set(participant_ids))

        # Fetch users by the provided UUIDs
        users = User.objects.filter(user_id__in=participant_ids)

        if not users.exists():
            raise ValidationError({"participants": "At least one valid participant is required."})

        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.

    - list: list messages (optionally filtered by conversation)
    - create: send a new message in an existing conversation
    """

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return messages from conversations that the user participates in.

        Optional query param:
        - ?conversation=<conversation_id> to filter messages by conversation.
        """
        user = self.request.user
        queryset = Message.objects.filter(
            conversation__participants=user
        ).select_related("sender", "conversation")

        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)

        return queryset.order_by("sent_at")

    def perform_create(self, serializer):
        """
        Send a message in an existing conversation.

        Expected payload:
        {
            "conversation": "<conversation_id>",
            "sender_id": "<user_id>",  # optional, we will override with request.user
            "message_body": "Hello!"
        }

        The sender is always set to the authenticated user.
        The user must be a participant of the conversation.
        """
        conversation = serializer.validated_data.get("conversation")

        # Ensure the conversation exists and the user is a participant
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)

