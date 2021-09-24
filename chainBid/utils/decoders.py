from dateutil import parser
from json import JSONDecoder


class DateTimeDecoder(JSONDecoder):
    """
    Datetime decoder for json serializer.

    usage:
    x = str(datetime.now())
    json.loads(x, cls=DateTimeDecoder)
    """

    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, source):
        for k, v in source.items():
            if isinstance(v, str):
                try:
                    source[k] = parser.isoparse(v)
                except:
                    pass
        return source
