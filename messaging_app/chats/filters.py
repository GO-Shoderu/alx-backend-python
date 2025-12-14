# chats/filters.py
import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Filter class for messages.

    Supports:
    - conversation: filter messages in a specific conversation
    - sender: filter messages by sender (user_id)
    - sent_after: messages sent at or after this datetime
    - sent_before: messages sent at or before this datetime
    """

    conversation = django_filters.UUIDFilter(
        field_name="conversation__conversation_id"
    )
    sender = django_filters.UUIDFilter(
        field_name="sender__user_id"
    )
    sent_after = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    sent_before = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["conversation", "sender", "sent_after", "sent_before"]
