"""
This module contains functions for subscriptions model
"""
from __future__ import annotations
from typing import List
from datetime import datetime, timezone, timedelta
from django.db.models import QuerySet
from .models import Subscriptions, MastersSubscriptions


def get_subscription_by_type(subscription_type: Subscriptions.Status) -> Subscriptions:
    """Return subscription object by type
    :param subscription_type: type of subscription
    :return: instances of class Subscription
    :rtype: Subscription
    """
    return Subscriptions.objects.get(type=subscription_type)


def get_subscription_by_id_or_none(subscription_id: int) -> Subscriptions | None:
    """

    """
    return Subscriptions.objects.filter(id=subscription_id).first()


def get_trial_subscription() -> Subscriptions:
    """Return trial subscription
    :return: instances of class Subscription
        (type of the instance is SubscriptionTypes.TRIAL)
    :rtype: Subscription
    """
    return get_subscription_by_type(Subscriptions.Types.TRIAL.value)


def save_master_subscription(master_id: int, subscription_id: int,
                             start_date: datetime, end_date: datetime,
                             status: MastersSubscriptions.Status,
                             paying_price: int) -> MastersSubscriptions:
    """

    """
    return MastersSubscriptions.objects.create(
        master_id=master_id,
        subscription_id=subscription_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
        paying_price=paying_price
    )


def save_master_trial_subscription(master_id: int) -> MastersSubscriptions:
    """

    """
    trial_subscription = get_trial_subscription()
    start_date = datetime.now(timezone.utc)
    end_date = start_date + timedelta(days=60)
    return MastersSubscriptions.objects.create(
        master_id=master_id,
        subscription_id=trial_subscription.pk,
        start_date=start_date,
        end_date=end_date,
        status=MastersSubscriptions.Status.ACTIVE.value
    )


def get_master_subscriptions(master_id: int) -> QuerySet[MastersSubscriptions]:
    """

    """
    return MastersSubscriptions.objects.select_related('subscription').filter(master_id=master_id)


def get_active_master_subscription_or_none(master_id: int) -> MastersSubscriptions | None:
    """

    """
    return MastersSubscriptions.objects.filter(
        master_id=master_id,
        status=MastersSubscriptions.Status.ACTIVE.value
    ).first()


def get_paid_master_subscriptions(master_id: int) -> List[MastersSubscriptions]:
    """Returns list of paid subscriptions order by -start_date
    """
    return MastersSubscriptions.objects.filter(
        master_id=master_id,
        status=MastersSubscriptions.Status.PAID.value
    ).order_by('-start_date')


def get_subscription_end_time(start_date: datetime, days: int) -> datetime:
    """

    """
    end_time = start_date + timedelta(days=days)
    return end_time

