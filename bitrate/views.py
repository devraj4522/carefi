from django.http.request import QueryDict

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.pagination import PageNumberPagination
from .models import Bitcoin
from .serializers import BitcoinAccountSerializers, BitcoinAccountSerializers_1

from auth_api.response import format_response

from rest_framework.decorators import api_view
from auth_api.permissions import user_permissions

import logging
infoLog = logging.getLogger('info')
errorLog = logging.getLogger('error')


class HomePage(APIView):
    def get(self, request):
        return Response(format_response("Home Page"))


@api_view(http_method_names=['POST'])
def current_price(request):
    if request.method == "POST":
        try:
            """
            An API for fetching the price of Bitcoin in real time.
            Fetch the prices and store in the database.
            """
            user = user_permissions(request)
            if not user:
                return Response(format_response({'message': "User Not Logged In"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            # defining key/request url
            key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

            # requesting data from url
            data = requests.get(key)
            data = json.loads(data.text)
            new_data = dict()
            new_data['price'] = float(data['price'])
            data = new_data

            # input_data = QueryDict.dict(request.data)
            input_data = QueryDict.dict(data)

            serialized_var = BitcoinAccountSerializers(data=input_data)

            if serialized_var.is_valid():
                serialized_var.save()
                context = {
                    'message': 'Succesfully fetched and added to database',
                    'Details': serialized_var.data,
                }
                return Response(format_response(context))
            else:
                context = {
                    'message': f"{serialized_var.errors}",
                }
                return Response(format_response(context, 400), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            errorLog.error(f"Bad Response Recieved while fetching data:{e}")
            return Response(format_response({'message': f"Exception while fetching data:{e}"}, 400),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(format_response({'message': "Invalid Request"}, 400), status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def get_price_list_details(request):
    if request.method == "GET":
        try:

            user = user_permissions(request)
            if not user:
                return Response(format_response({'message': "User Not Logged In"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            paginator = PageNumberPagination()
            enquiry_qs = Bitcoin.objects.all()
            total_count = enquiry_qs.count()

            result_page = paginator.paginate_queryset(enquiry_qs, request)
            serialized_var = BitcoinAccountSerializers_1(
                result_page, many=True).data

            if not request.GET.get('page'):
                return Response(format_response({"message": "(DC-0003) Provide the page number. eg: ?page=1"}, 400),
                                status=status.HTTP_400_BAD_REQUEST)

            page_num = request.GET.get('page')
            if paginator.get_next_link() == None:
                next_page_number = None
            else:
                next_page_number = int(page_num) + 1

            if paginator.get_previous_link() == None:
                previous_page_number = None
            else:
                previous_page_number = int(page_num) - 1

            context = {
                'message': 'Enquiry details fetched successfully',
                'count': total_count,
                'next_page_number': next_page_number,
                'previous_page_number': previous_page_number,
                'enquiry_details': serialized_var
            }
            return Response(format_response(context))

        except Exception as e:
            errorLog.error(
                f"Bad Response Recieved while fetching all the Enquiry details :{e}")
            return Response(format_response({'message': f"(DC-0005) Exception while fetchig enquiry details: {e}"}, 400),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(format_response({'message': "(DC-0008) Invalid Request"}, 400), status=status.HTTP_400_BAD_REQUEST)
