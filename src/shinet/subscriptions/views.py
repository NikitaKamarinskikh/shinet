from rest_framework.generics import ListAPIView
from .serializers import SubscriptionSerializer
from .models import Subscriptions


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionSerializer






