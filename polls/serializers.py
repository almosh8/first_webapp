import json

from dateutil.parser import isoparse


def get_dict_from_json(json_data):
    return json.loads(json_data)


def get_json_from_dict(dict_data):
    return json.dumps(dict_data)


def get_date_from_string(date_string):
    return isoparse(date_string)
