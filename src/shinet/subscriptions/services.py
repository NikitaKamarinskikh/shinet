"""
This module contains functions for subscriptions model
"""
from .models import Subscriptions
from .settings import SubscriptionTypes


def get_subscription_by_type(subscription_type: SubscriptionTypes) -> Subscriptions:
    """Return subscription object by type
    :param subscription_type: type of subscription
    :return: instances of class Subscription
    :rtype: Subscription
    """
    return Subscriptions.objects.get(type=subscription_type.name)


def get_trial_subscription() -> Subscriptions:
    """Return trial subscription
    :return: instances of class Subscription
        (type of the instance is SubscriptionTypes.TRIAL)
    :rtype: Subscription
    """
    return get_subscription_by_type(SubscriptionTypes.TRIAL)





