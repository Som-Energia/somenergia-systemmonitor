import time
import smtplib
import datetime
from email.mime.text import MIMEText
import requests

GMAIL_USER = ""
GMAIL_PASSWORD = ""

def send_report(subject, results):
    _from = GMAIL_USER
    _to = GMAIL_USER
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASSWORD)

    content = ""
    for (fail_con, fail_test, fail_output, _time, _timeout, test_name) in results:
        content += """
Name:{test_name}
Status (connection): {fail_con}
Status (test): {fail_test}
Time: {_time}
Timeout: {_timeout}
Output: {fail_output}\n\n""".format(**locals())

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER

    
    server.sendmail(_from, _to, msg.as_string())
    server.quit()


def run_test(func, timeout):
    start_time = time.time()
    result = func()
    end_time = time.time()
    duration = end_time - start_time
    result += (duration, duration<timeout, func.__name__, )
    return result


def get_ip():
    url = "http://checkip.dyndns.org"
    rply = requests.get(url)
    clean = rply.text.split(': ', 1)[1]
    return clean.split('</body></html>', 1)[0]

def push_test(subject, results):
    # failed = False
    # for (fail_con, fail_test, fail_output, _time, _timeout, test_name) in results:
    #     if not fail_con or _timeout:
    #         failed = True
    # if failed:
    #     send_report(subject + ' ' + get_ip(), results)
    send_report(subject + ' ' + get_ip(), results)
