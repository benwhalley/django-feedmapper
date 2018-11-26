"""
JSONField automatically serializes most Python terms to JSON data.
Creates a TEXT field with a default value of "{}".  See test_json.py for
more information.

 from django.db import models
 from django_extensions.db.fields import json

 class LOL(models.Model):
     extra = json.JSONField()
"""

import datetime
from decimal import Decimal
from django.db import models
from django.conf import settings
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            assert settings.TIME_ZONE == 'UTC'
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        return json.JSONEncoder.default(self, obj)


def dumps(value):
    assert isinstance(value, dict)
    return JSONEncoder(indent=4).encode(value)


def loads(txt):
    value = json.loads(
        txt,
        parse_float=Decimal,
        encoding=settings.DEFAULT_CHARSET
    )
    assert isinstance(value, dict)
    return value


class JSONDict(dict):
    """
    Hack so repr() called by dumpdata will output JSON instead of
    Python formatted data.  This way fixtures will work!
    """
    def __repr__(self):
        return dumps(self)


