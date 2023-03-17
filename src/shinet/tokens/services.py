from .models import RefreshTokens


def create_refresh_token(user_id: int, token: str) -> RefreshTokens:
    return RefreshTokens.objects.create(user_id=user_id, token=token)




