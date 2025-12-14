from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to ensure that:

    - Only authenticated users can access the API.
    - Only participants in a conversation can view, send, update,
      or delete messages in that conversation.
    """

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
          conversation.
        """
        user = request.user

        # Conversation instance
        if isinstance(obj, Conversation):
            return obj.participants.filter(pk=user.pk).exists()

        # Message instance
        if isinstance(obj, Message):
            return obj.conversation.participants.filter(pk=user.pk).exists()

        # Any other object type: deny
        return False