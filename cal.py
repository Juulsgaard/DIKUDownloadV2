import urllib.request
import icalendar
from datetime import datetime, timezone, timedelta
import pytz
import math
import re

username = "xcn534"

cal_url = "https://personligtskema.ku.dk/ical.asp?objectclass=student&id=%s" % username
cal_file = urllib.request.urlopen(cal_url)

events = icalendar.Calendar.from_ical(cal_file.read())
# now = datetime.now(tz=pytz.timezone("Europe/Copenhagen"))
now = datetime(2018, 9, 7, 7, 15, 0, 0, timezone.utc)

current_class = None
next_class = None

for event in events.walk("vevent"):
    end = event['DTEND'].dt
    if end < now:
        continue

    start = event['DTSTART'].dt
    if start.month >= now.month and start.day > now.day: break

    if start < now:
        current_class = event
    else:
        next_class = event
        break


def print_class(cal_event):
    title = re.sub(r'^.+;', '', cal_event["SUMMARY"])
    title_g = re.search(r' ?- ?(\w+) ?$', title)
    class_type = title_g.group(1)
    title = re.sub(r' ?- ?\w+ ?$', '', title)

    start = cal_event['DTSTART'].dt
    end = cal_event['DTEND'].dt
    duration = end - start

    print(title)
    print("Type: %s" % class_type)
    print("Tid: %i timer" % math.ceil(duration.seconds / 3600))

    if start < now:
        print("Tid tilbage: %s" % (end - now))
    else:
        print("Tid før start: %s" % str((start + timedelta(minutes=15)) - now))

    description = cal_event["DESCRIPTION"]

    room_g = re.search(r'Room: (.+?)\. ?\n', description)
    if room_g:
        room = room_g.group(1)
        print("Lokale: %s" % room)

    prof_g = re.search(r'Staff: (.+?)\. ?\n', description)
    if prof_g:
        prof = prof_g.group(1).strip().split(",")
        prof = " ".join(list(reversed(prof))).strip()
        print("Underviser: %s" % prof)


print_class(current_class)
print()
print_class(next_class)
