from datetime import datetime

import pytz

from diku_tools.calendars import LectureEvent, Calendar

now = datetime.now(tz=pytz.timezone("Europe/Copenhagen"))
# now = datetime(2018, 9, 13, 7, 15, 0, 0)


def print_var(prefix, var_name, value):
    print("%s%s=%s" % (prefix, var_name, value))


def print_class(event: LectureEvent, prefix):

    if event is None:
        print_var("Show", prefix, 0)
        return

    print_var("Show", prefix, 1)

    print_var(prefix, "Title", event.get_title())
    print_var(prefix, "Type", event.get_type())
    print_var(prefix, "Duration", event.get_duration())
    print_var(prefix, "Remainder", event.get_end_delta(now))
    print_var(prefix, "Countdown", event.get_start_delta(now))
    print_var(prefix, "Room", event.get_room())
    print_var(prefix, "Professor", event.get_prof())


cal = Calendar(username="xcn534")

print("[Variables]")
print_class(cal.get_current(now), "Current")
print()
print_class(cal.get_next(now), "Next")
