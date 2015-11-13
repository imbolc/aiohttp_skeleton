import datetime
from lib.web import jsonify


async def now(request):
    return jsonify(
        [
            'Test of json response and datetime serialization',
            {
                'curent': {'utc_time': datetime.datetime.utcnow()},
            }
        ]
    )
