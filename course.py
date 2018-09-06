import os

from tools import api_call, create_dir, clean_dir, download_file, clean_file, create_shortcut


def download_course(course_id, base_path, session):
    root = api_call("courses/%i/folders/root" % course_id, session)
    get_course_files(root["id"], base_path, session)

    modules = api_call("courses/%i/modules" % course_id, session)
    get_modules(modules, base_path, course_id, session)

    announcements = api_call("announcements?context_codes[]=course_%i" % course_id, session)
    announcement_path = base_path + "#ANNOUNCEMENTS/"
    create_dir(announcement_path)
    for announcement in announcements:
        time = announcement["posted_at"][:10]
        name = "%s %s.html" % (time, announcement["title"])
        file_path = announcement_path + name
        if os.path.isfile(file_path):
            continue
        file = open(file_path, "w")
        file.write(announcement["message"])
        file.close()


def get_course_files(folder_id, path, session):
    print(path)
    create_dir(path)

    files = api_call("folders/%i/files" % folder_id, session)
    folders = api_call("folders/%i/folders" % folder_id, session)

    for file in files:
        download_file(path + clean_file(file["display_name"]), file["url"], session)

    for folder in folders:
        get_course_files(folder["id"], path + clean_dir(folder["name"]), session)


def get_modules(modules, path, course_id, session):
    path = path + "#MODULES/"
    create_dir(path)
    for module in modules:
        module_path = path + clean_dir(module["name"])
        create_dir(module_path)

        items = api_call("courses/%i/modules/%i/items" % (course_id, module["id"]), session)

        header = None
        for item in items:
            item_type = item["type"]
            new_path = module_path + (header if header else "")

            if item_type == "SubHeader":
                header = clean_dir(item["title"])
                create_dir(module_path + header)
            elif item_type == "File":
                file = api_call("files/%i" % item["content_id"], session)
                download_file(new_path + clean_file(file["display_name"]), file["url"], session)
            elif item_type in ["Quiz", "Assignment", "External_Link", "Page"]:
                create_shortcut(new_path + clean_file(item["title"]), item["html_url"])

