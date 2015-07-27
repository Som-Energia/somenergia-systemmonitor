import helpscout
import urllib2
import time
import requests
import base64
import json
import re
import socket
import datetime
from check import send_report, run_test, push_test

# WARNING: To be updated with proper settings
API_KEY = ""

def test_list_mailboxes():
    '''
    WARNING: To be updated with proper data
    '''

    _mailboxes = []
    try:
        client = helpscout.Client()
        client.api_key = API_KEY
        mailboxes = client.mailboxes().items
        _mailboxes = [mailbox.name for mailbox in mailboxes]
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        return False, False, None
    except Exception as e:
        return True, False, None

    return (True, _mailboxes ==
                     [], None) # To be updated


def test_list_users():
    '''
    WARNING: To be updated with proper data
    '''

    _mailboxes = []
    try:
        client = helpscout.Client()
        client.api_key = API_KEY
        users = client.users().items
        _users = [user.email for user in users]
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        return (False, False, None)
    except Exception as e:
        return (True, False, None)

    return (True, _users == \
                    [], None) # To be updated


def _url_req(url):
    req = urllib2.Request(url)
    authheader =  "Basic %s" % base64.encodestring('%s:%s' % (API_KEY, "DUMMY_PASSWORD"))
    req.add_header("Authorization", authheader)
    rply = urllib2.urlopen(req)
    content = rply.read()
    return json.loads(content)


def test_list_collections():
    '''
    WARNING: To be updated with proper data
    '''

    url = 'https://docsapi.helpscout.net/v1/collections'
    try:
        content = _url_req(url)
        _collections = [collection['name'] for collection in content['collections']['items']]
    except urllib2.URLError as e:
        return True, False, None
    except socket.timeout, e:
        return False, False, None
    return (True, True, _collections == \
        [], None) # To be updated


def test_get_doc():
    url_articles = 'https://docsapi.helpscout.net/v1/articles/'
    article_id = ''
    url = url_articles + article_id
    try:
        content = _url_req(url)
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          content['article']['text'])
        for url in urls:
            response = urllib2.urlopen(url)
            dummy = response.read()
        return True, True,None
    except urllib2.URLError as e:
        return True, False,None
    except socket.timeout, e:
        return False, False, None


results = []
results.append(run_test(test_list_mailboxes, 2))
results.append(run_test(test_list_users, 2))
results.append(run_test(test_list_collections, 2))
results.append(run_test(test_get_doc, 20))

push_test('Help Scout status %s' % datetime.datetime.now(), results)
