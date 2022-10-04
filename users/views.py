from django.http.request import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password, make_password

from .models import User
from .serializers import UserAccountSerializers, UserAccountSerializers_1

from auth_api.encryption import generating_jwt_token, jwt_payload_generate
from auth_api.response import format_response

from rest_framework.decorators import api_view

import logging
infoLog = logging.getLogger('info')
errorLog = logging.getLogger('error')


class HomePage(APIView):
    def get(self, request):
        return Response(format_response("Home Page"))


@api_view(http_method_names=['POST'])
def user_signup(request):
    if request.method == "POST":
        try:
            input_data = QueryDict.dict(request.data)
            """
            checking if the email and password are providing or not . If not displaying error mesg.
            checking the entered  email-id or not . If not displaying the error mesg else insert the data into the table
            """

            if 'email' not in input_data:
                return Response(format_response({'message': " Email and password are mandatory!..."}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            if 'password' in input_data:
                if not input_data['password']:  # cheking if they provide '' value
                    return Response(format_response({'message': " Provide the value for password field"}, 400),
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(format_response({'message': "Provide the password"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            # removing white spaces
            input_data['email'] = input_data['email'].strip()

            original_password = input_data['password']
            input_data['password'] = make_password(
                input_data['password'])  # encrypting the password

            if 'username' not in input_data:  # if username not provided , create by spliting the email
                input_data['username'] = input_data['email'].split('@')[0]

            user_data = User.objects.filter(
                email__iexact=input_data['email'])  # query user from model db
            if user_data.exists() != True:
                serialized_var = UserAccountSerializers(data=input_data)
                if serialized_var.is_valid():
                    serialized_var.save()

                    user = User.objects.get(
                        id=serialized_var.data['id'])

                    """ generating token """
                    payload = jwt_payload_generate(
                        user.id)
                    token = generating_jwt_token(payload)

                    user_serialized_var = UserAccountSerializers_1(user).data
                    context = {
                        'message': 'Successfully registered.',
                        'token': token,
                        'UserDetails': user_serialized_var,
                    }
                    return Response(format_response(context, 201), status=status.HTTP_201_CREATED)
                else:
                    context = {
                        'message': f"(DC-0010) {serialized_var.errors}",
                    }
                    return Response(format_response(context, 400), status=status.HTTP_400_BAD_REQUEST)
            else:
                context = {
                    'message': 'Email-id already registered.',
                }
                return Response(format_response(context, 400), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            errorLog.error(f"Bad Response Recieved while user signing up:{e}")
            return Response(format_response({'message': f"Exception while user signing up:{e}"}, 400),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(format_response({'message': "Invalid Request"}, 400), status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
def user_login(request):
    if request.method == "POST":
        try:
            """
            checking if the email and password are providing or not . If not displaying error mesg.
            checking the entered  email-id or not . If not displaying the error mesg .
            """
            input_data = QueryDict.dict(request.data)
            if 'email' not in input_data:
                return Response(format_response({'message': "(DC-0003) Provide the email-id"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            if 'password' not in input_data:
                return Response(format_response({'message': "(DC-0003) Provide the password"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            # removing white spaces
            input_data['email'] = input_data['email'].strip()

            if User.objects.filter(email__iexact=input_data['email']).exists() == True:
                user = is_authenticate(
                    input_data['email'], input_data['password'])
                if user:
                    """ generating token """
                    payload = jwt_payload_generate(
                        user.id)
                    token = generating_jwt_token(payload)

                    serialized_var = UserAccountSerializers_1(user).data
                    context = {
                        'message': 'Succesfully loggedin',
                        'token': token,
                        'UserDetails': serialized_var,
                    }
                    return Response(format_response(context))
                else:
                    context = {
                        'message': 'Unable to login with provided credentials',
                    }
                    return Response(format_response(context, 400), status=status.HTTP_400_BAD_REQUEST)
            else:
                context = {
                    'message': 'Email does not exist!...',
                }
                return Response(format_response(context, 400), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            errorLog.error(f"Bad Response Recieved while user login:{e}")
            return Response(format_response({'message': f"Exception while user login:{e}"}, 400),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(format_response({'message': "Invalid Request"}, 400), status=status.HTTP_400_BAD_REQUEST)


def is_authenticate(email_id, password):
    """
    Authenticate the user
    1. on the basis of email + password : parameters email-id and password : required(email , password)
    return: if success user object, otherwise pass
    """
    try:
        user = User.objects.get(
            email__iexact=email_id)
        if check_password(password, user.password):
            return user

    except ObjectDoesNotExist:
        pass
