#!/usr/bin/env python
# @Author  : pengyun


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'mongo server'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

schema = {
    'compound': {
        'type': 'string',
    },
    'href': {
        'type': 'string'
    },
    'number': {
        'type': 'string'
    },
    'img_url': {
        'type': 'list',
    },
    'location': {
        'type': 'list',
    },
}

resource = {
    'item_title': 'house',
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'schema': schema,
}


DOMAIN = {
    'resource url': resource,
}
