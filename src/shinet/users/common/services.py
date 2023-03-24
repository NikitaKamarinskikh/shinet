"""
This module contains functions for
"""
from __future__ import annotations
from hashlib import sha256
from users.models import Users


def make_sha256_hash(string: str) -> str:
    return sha256(string.encode('utf-8')).hexdigest()


def get_user_by_email_or_none(email: str) -> str | None:
    return Users.objects.filter(email=email).first()

