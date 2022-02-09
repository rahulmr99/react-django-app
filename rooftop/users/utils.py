from rest_framework.authtoken.models import Token


def get_tokens_for_user(user):
    """
    Function to generate token for User
    :param user: user
    :return:
    """
    refresh = Token.objects.get(user=user)

    return {
        'access': str(refresh.key),
    }
