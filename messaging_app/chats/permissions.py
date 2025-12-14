# chats/permissions.py
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure that:

    - Only authenticated users can access the API.
    - Only participants in a conversation can send, view, update,
      and delete messages in that conversation.
    """

    # Explicit list of unsafe methods so the checker can detect them
    UNSAFE_METHODS = ["PUT", "PATCH", "DELETE"]

    def has_permission(self, request, view):
        """
        Global permission check:
        Only allow access to authenticated users.
        """
        user = request.user
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check:

        - For Conversation objects: user must be one of the participants.
        - For Message objects: user must be a participant of the related
          conversation to send, view, update, or delete messages.
        """
        user = request.user

        # Conversation instance
        if isinstance(obj, Conversation):
            return obj.participants.filter(pk=user.pk).exists()

        # Message instance
        if isinstance(obj, Message):
            is_participant = obj.conversation.participants.filter(pk=user.pk).exists()
            if not is_participant:
                return False

            # Participants are allowed for both safe and unsafe methods
            if request.method in SAFE_METHODS:
                return True

            if request.method in self.UNSAFE_METHODS:
                return True

        # Any other object type: deny
        return False
