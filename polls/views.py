import datetime
import json
from dateutil.parser import isoparse
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime as dt

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from my_web_app import settings
import pytz

from polls.models import Offer, Category
from polls.serializers import ItemSerializer, MyDeserializer, MySerializer

SUCCESS_CODE = 200


def index(request):
    return HttpResponse("Time now is ")


@api_view(['POST'])
# @parser_classes([JSONParser])
def add_items(request):
    data_json = request.body.decode('utf8')  # decode bytes to JSON
    print(f'import request with data={data_json}')
    deserializer = MyDeserializer(json_data=data_json)
    batch = deserializer.get_dict()



    return Response(status=SUCCESS_CODE)

@api_view(['GET', 'DELETE'])
def delete(request, pk):
    try:
        item = Category.objects.get(pk=pk)
    except ObjectDoesNotExist:
        try:
            item = Offer.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse('{"code": 404,"message": "Item not found"}', status=404)

    if item.parent_category is not None:
        item.parent_category.remove_child(item)
    item.delete()


    return HttpResponse(status=SUCCESS_CODE)

@api_view(['GET'])
def nodes(request, pk):
    try:
        item = Category.objects.get(pk=pk)
    except ObjectDoesNotExist:
        try:
            item = Offer.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse('{"code": 404,"message": "Item not found"}', status=404)

    serializer = ItemSerializer(item)
    json_data = serializer.get_json()

    return HttpResponse(json_data, status=SUCCESS_CODE)

@api_view(['GET'])
def sales(request):

    try:
        date_str = request.GET['date']
        print(f'sales request with date = {date_str}')
        date_end = isoparse(date_str)
    except ValueError:
        return HttpResponse('{"code": 400,"message": "Validation Failed"}', status=400)

    date_start = date_end - datetime.timedelta(days=1)

    offers = Offer.objects.filter(update_date__range=(date_start, date_end))
    offers_dicts = []
    for offer in list(offers):
        serializer = ItemSerializer(offer, include_children=False)
        offer_dict = serializer.get_dict()
        offers_dicts.append(offer_dict)

    data_dict = {'items': offers_dicts}
    serializer = MySerializer(data_dict)
    data_json = serializer.get_json()
    return HttpResponse(data_json, status=SUCCESS_CODE)

@api_view(['GET'])
def statistic(request, pk):
    return HttpResponse('{}', status=SUCCESS_CODE)
