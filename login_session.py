import json

import requests
import lxml.html


def session_login():
    login_url = "https://federation.ku.dk/CookieAuth.dll?Logon"
    url = "https://absalon.ku.dk/login"

    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    login = session.get(url)

    login_html = lxml.html.fromstring(login.text)
    hidden_elements = login_html.xpath('//input[@type="hidden"]')
    form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

    with open('config.json') as f:
        login_config = json.load(f)

    form['username'] = login_config["username"]
    form['password'] = login_config["password"]
    form['trusted'] = "4"

    session.headers.update({'referer': login.url})
    response = session.post(login_url, data=form)

    saml_html = lxml.html.fromstring(response.text)
    hidden_elements = saml_html.xpath('//input[@type="hidden"]')
    form_element = saml_html.xpath('//form')
    form = {x.attrib['name']: x.attrib['value'] for x in hidden_elements}

    session.post(form_element[0].attrib["action"], data=form)

    return session
