from datetime import datetime


def datetime_to_iso(obj):
    '''datetime_to_iso datetime to ISO string'''
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: datetime_to_iso(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [datetime_to_iso(v) for v in obj]
    return obj
