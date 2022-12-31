import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from polls.controllers.DELETE_controllers.delete_controller.items_remover import remove_item_subtree
from polls.controllers.GET_controllers.export_controller.items_exporter import get_export_item_subtree_dict
from polls.controllers.POST_controllers.import_controller import *
from polls.controllers.POST_controllers.import_controller.items_importer import ItemsImporter
from polls.models import Offer, Category
from polls.serializers import *

SUCCESS_CODE = 200


@api_view(['POST'])
def add_items(request):
    batch_dict = get_dict_from_request(request)
    print(f'import request with data={batch_dict}')

    items_importer = ItemsImporter(batch_dict)
    items_importer.import_items()

    return Response(status=SUCCESS_CODE)


def get_dict_from_request(request):
    data_json = request.body.decode()  # decode bytes to JSON

    batch_dict = get_dict_from_json(data_json)
    return batch_dict


@api_view(['GET', 'DELETE'])
def delete(request, pk):
    remove_item_subtree(pk)

    return HttpResponse(status=SUCCESS_CODE)


@api_view(['GET'])
def export_items(request, pk):
    export_data_dict = get_export_item_subtree_dict(pk)
    json_data = get_json_from_dict(export_data_dict)

    return HttpResponse(json_data, status=SUCCESS_CODE)


@api_view(['GET'])
def sales(request):
    date_str = request.GET['date']
    print(f'sales request with date = {date_str}')
    date_end = isoparse(date_str)

    export_data_dict = get_export_item_subtree_dict(pk)
    json_data = get_json_from_dict(export_data_dict)

    data_json = get_json_from_dict()
    return HttpResponse(data_json, status=SUCCESS_CODE)


@api_view(['GET'])
def statistic(request, pk):
    return HttpResponse('{}', status=SUCCESS_CODE)
