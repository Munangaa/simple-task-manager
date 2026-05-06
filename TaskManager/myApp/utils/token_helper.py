from datetime import datetime

from django.contrib.auth import tokens


def get_user_from_token(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    token_data = tokens.get(token)

    if not token_data:
        return None, 'Invalid token'


    if datetime.now() > token_data['expires_at']:
        del tokens[token]  # remove expired token
        return None, 'Token expired'

    return token_data['user_id'], None