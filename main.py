import json
import os
import re

from diku_tools.course import Course
from diku_tools.canvas_session import CanvasSession
from diku_tools.tools import create_dir, clean_dir

config = {}
if os.path.isfile("config.json"):
    with open('config.json') as f:
        config = json.load(f)

config_changed = False

if "username" not in config or not config["username"]:
    data = input("Username: ")
    config["username"] = data
    config_changed = True

if "password" not in config or not config["password"]:
    data = input("Password: ")
    config["password"] = data
    config_changed = True

if "save_location" not in config or not config["save_location"]:
    data = input("Save location: ")
    config["save_location"] = data
    config_changed = True

if config_changed:
    conf_file = open("config.json", "w")
    conf_file.write(json.dumps(config))
    conf_file.close()

save_path = config["save_location"]
save_path = re.sub(r'(?:\\|/*$)', '/', save_path)

session = CanvasSession(username=config["username"], password=config["password"])

course_names = {
    "Diskret matematik og algoritmer": "DMA",
    "Programmering og problemløsning": "PoP"
}

create_dir(save_path)

courses = session.api_call("courses")

for course in courses:
    course_name = course["name"]
    for name, short in course_names.items():
        if name in course["name"]:
            course_name = short
            break

    new_path = save_path + clean_dir(course_name)
    create_dir(new_path)
    Course(course_id=course["id"], path=new_path, session=session).download()

