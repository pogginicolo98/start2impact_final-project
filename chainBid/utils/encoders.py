from datetime import datetime
from decimal import Decimal
from json import JSONEncoder


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
