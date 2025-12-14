from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Conversation, Message


class IsConversationParticipant(BasePermission):
    """
    Permission to ensure the user is a participant in the conversation
    related to the object.

    - For Conversation objects:
        Allow access only if the requesting user is in participants.
    - For Message objects:
        Allow access only if the requesting user is in the participants
        of the related conversation.
    - For unsafe methods on Message (PATCH, PUT, DELETE):
        Additionally require that the user is the sender.
    """

    def has_permission(self, request, view):
        """
        Called before has_object_permission.
        At this stage, we just enforce that the user is authenticated.
        The more specific checks happen in has_object_permission.
        """
        user = request.user
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        """

        user = request.user

        # Conversation instance
        if isinstance(obj, Conversation):
            # User must be one of the participants
            return obj.participants.filter(pk=user.pk).exists()

        # Message instance
        if isinstance(obj, Message):
            # First: must be a participant of the conversation
            is_participant = obj.conversation.participants.filter(pk=user.pk).exists()
            if not is_participant:
                return False

            # For read-only methods (GET, HEAD, OPTIONS), allow all participants
            if request.method in SAFE_METHODS:
                return True

            # For write methods (PATCH, PUT, DELETE), only the sender can modify
            return obj.sender_id == user.pk

        # If the object is of some other type, deny by default
        return False
