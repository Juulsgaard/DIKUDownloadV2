import json
import os
import re
import platform

api_url = "https://absalon.ku.dk/api/v1/"


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def clean_dir(dir_name):
    dir_name = dir_name.replace(':', ' -').replace('/', '-').replace('...', '').strip()
    return re.sub(r'/*$', '/', dir_name)


def clean_file(file_name):
    return file_name\
        .replace(':', ' -')\
        .replace('/', '-')\
        .replace('...', '')\
        .strip()


def api_call(call, session):
    data = session.get(api_url + call)
    data = data.text.replace('while(1);', '')
    return json.loads(data)


def download_file(path, url, session):
    if not url or os.path.isfile(path):
        return

    r = session.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def create_shortcut(path, url):
    if os.path.isfile(path + ".bat") or os.path.isfile(path + ".sh"):
        return

    if platform.system() == "Windows":
        file = open(path + ".bat", "w")
    else:
        file = open(path + ".sh", "w")

    file.write('start "" "%s"' % url)
    file.close()
