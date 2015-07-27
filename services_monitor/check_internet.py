import urllib2
import time
import requests
import base64
import datetime
import subprocess
from check import send_report, run_test, push_test

def test_internet():
    p = subprocess.Popen(['/bin/sh','check_internet.sh'], stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    out, err = p.communicate()
    return True, True, out.replace(r'\n','\n<br>')

results = []
results.append(run_test(test_internet, 1000))

push_test('Internet status %s' % datetime.datetime.now(), results)
