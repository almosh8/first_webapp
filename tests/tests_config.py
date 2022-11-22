import json

IMPORT_BATCHES_DICT = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            },
            {
                "type": "CATEGORY",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
            {
                "type": "OFFER",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 128
            },
            {
                "type": "OFFER",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 256
            }
        ],
        "updateDate": "2022-02-02T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            },
            {
                "type": "OFFER",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 512
            },
            {
                "type": "OFFER",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 1024
            }
        ],
        "updateDate": "2022-02-03T12:00:00Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 64
            }
        ],
        "updateDate": "2022-02-03T15:00:00Z"
    }
]
EXPECTED_TREE = {
    "type": "CATEGORY",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 1984,
    "parentId": None,
    "date": "2022-02-03T15:00:00Z",
    "children": [
        {
            "type": "CATEGORY",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 1600,
            "date": "2022-02-03T15:00:00Z",
            "children": [
                {
                    "type": "OFFER",

                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 512,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 1024,
                    "date": "2022-02-03T12:00:00Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 64,
                    "date": "2022-02-03T15:00:00Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 384,
            "date": "2022-02-02T12:00:00Z",
            "children": [
                {
                    "type": "OFFER",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 128,
                    "date": "2022-02-02T12:00:00Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 256,
                    "date": "2022-02-02T12:00:00Z",
                    "children": None
                }
            ]
        },
    ]
}

IMPORT_ITEMS_DICT = IMPORT_BATCHES_DICT[0]
TEST_CATEGORY_DICT = IMPORT_ITEMS_DICT['items'][0]
TEST_OFFER_DICT = IMPORT_ITEMS_DICT['items'][2]

EXPECTED_TREE_DICT = json.dumps(EXPECTED_TREE)
