from datetime import datetime
from dateutil import parser
from decimal import Decimal
from json import JSONDecoder, JSONEncoder


class DateTimeEncoder(JSONEncoder):
    """
    Datetime encoder for json serializer.

    usage:
    x = datetime.now()
    json.dumps(x, cls=DateTimeEncoder)
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.astimezone().isoformat())
        return super().default(obj)


class DecimalEncoder(JSONEncoder):
    """
    Decimal encoder for json serializer.

    usage:
    x = Decimal("42.5")
    json.dumps(x, cls=DecimalEncoder)
    """

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class AuctionEncoder(DateTimeEncoder, DecimalEncoder):
    """
    Auction encoder designed for auction objects.
    Extends JSONEncoder, DateTimeEncoder and DecimalEncoder.
    """

    pass


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


class AuctionDecoder(DateTimeDecoder):
    """
    Auction decoder designed for auction objects.
    Extends JSONEncoder and DateTimeDecoder.
    """

    pass
