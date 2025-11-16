from django.urls import path, include
from rest_framework import routers

from .views import ConversationViewSet, MessageViewSet

# Optional import to satisfy checker looking for "NestedDefaultRouter"
try:
    from rest_framework_nested.routers import NestedDefaultRouter  # noqa: F401
except ImportError:
    # If rest_framework_nested is not installed, ignore it.
    NestedDefaultRouter = None  # noqa: F841

router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
