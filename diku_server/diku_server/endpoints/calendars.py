from datetime import datetime
import json

import pytz
from flask import Blueprint

from diku_tools.calendars import Calendar
from ..tools import get_user

bp = Blueprint('calendar', __name__)


@bp.route("/calendar/today")
def calendar_today():
    user = get_user()
    calendar = Calendar(user["username"])
    now = datetime.now(tz=pytz.timezone("Europe/Copenhagen"))
    today = calendar.get_day(now.year, now.month, now.day)
    events = []
    for event in today:
        events.append(event.to_dict())
    return json.dumps(events)
