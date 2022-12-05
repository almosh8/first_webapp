import json


def get_dict_from_json(json_data):
    return json.loads(json_data)


def get_json_from_dict(dict_data):
    return json.dumps(dict_data)
