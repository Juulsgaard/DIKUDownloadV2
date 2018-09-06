import json
import re

from course import download_course
from login_session import session_login
from tools import create_dir, api_call, clean_dir

with open('config.json') as f:
    config = json.load(f)

save_path = config["save_location"]
save_path = re.sub(r'/*$', '/', save_path)

session = session_login()

course_names = {
    "Diskret matematik og algoritmer": "DMA",
    "Programmering og problemløsning": "PoP"
}


create_dir(save_path)

courses = api_call("courses", session)

for course in courses:
    course_name = course["name"]
    for name, short in course_names.items():
        if name in course["name"]:
            course_name = short
            break

    new_path = save_path + clean_dir(course_name)
    create_dir(new_path)

    download_course(course["id"], new_path, session)
