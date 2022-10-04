from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .response import format_response
from .encryption import decoding_jwt_token
from rest_framework import exceptions

from users.models import User
import logging
infoLogger = logging.getLogger('info')
errorLogger = logging.getLogger('error')


def index(request):
    return HttpResponse("Hello, world. You're at the auth index.")


def user_permissions(request):
    try:
        user_id = decoding_jwt_token(
            request.META['HTTP_AUTHORIZATION']
        )['id']
        user = User.objects.get(id=user_id, )
        return user

    except Exception as e:
        errorLogger.error(
            f"Exception while validating the user jwt token :{e}")
        raise exceptions.NotAuthenticated(format_response(
            {'message': 'Token is missing or is invalid'}, 403))
