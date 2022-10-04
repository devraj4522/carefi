from traceback import format_exc

import jwt
from django.conf import settings
from datetime import datetime, timedelta
import logging

infoLogger = logging.getLogger('info')
errorLogger = logging.getLogger('error')


def generating_jwt_token(payload):
    """return encoded jwt"""
    try:
        infoLogger.info('Encoding Payload')
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            'HS256'
        )
    except jwt.exceptions as e:
        errorLogger.error('Error while encoding')
        return None


def decoding_jwt_token(token):
    """return decoded jwt"""
    try:
        _options = {
            "verify_signature": True,
            "require": ["exp", "iat"],
            "verify_exp": True,
            "verify_iat": True
        }
        decoded = jwt.decode(
            jwt=token.split()[1],
            key=settings.SECRET_KEY,
            # options=_options,
            algorithms=['HS256'],
        )
        return decoded
    except jwt.exceptions.InvalidSignatureError as e:
        errorLogger.error('Unable to Decode')
        return None
    except jwt.exceptions.MissingRequiredClaimError:
        errorLogger.error(f'Missing Required Claims {format_exc()}')
        return None
    except jwt.exceptions.DecodeError as d:
        errorLogger.error(d)
        return None
    except jwt.exceptions:
        errorLogger.error(f'Unable to decode JWT {format_exc()}')
        return None


def jwt_payload_generate(user_id):
    """create payload"""
    exp_time = datetime.now() + timedelta(days=30)
    payload = {
        'id': user_id,
        # 'iat': datetime.now(),
        # 'exp': exp_time
    }
    return payload
