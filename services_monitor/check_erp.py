import time
import datetime
from ooop import OOOP
from check import send_report, run_test, push_test

# WARNING: To be updated with proper settings
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_URI = ''
DB_PORT = 8888

O = None

def test_connection():
    global O
    try:
        O = OOOP(dbname=DB_NAME, user=DB_USER, pwd=DB_PASSWORD, port=int(DB_PORT), uri=DB_URI)
    except Exception as e:
        return False, False, None
    return True, True, None


def test_users():
    if not O:
        return False, False, None

    user_obj = O.ResUsers
    try:
        user_ids = user_obj.search([])
        return True, user_ids == [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], None
    except Exception ,e:
        return False, False, None


def test_contracts():
    if not O:
        return False, False, None

    polissa_obj = O.GiscedataPolissa
    try:
        polissa_ids = polissa_obj.search([])
        return True, len(polissa_ids)>20000, None
    except Exception, e:
        return False, False, None


def test_billing():
    '''
    WARNING: To be updated will proper data
    '''
    if not O:
        return False, False, None

    billing_obj = O.GiscedataFacturacioFactura
    fields_to_read = ['origin', 'cups_id']
    return True, billing_obj.read([1000, 1010], fields_to_read) == \
        [{'origin': 'F0000000000000',
          'id': 1000,
          'cups_id': [100, 'ES00000000000000000000']},
         {'origin': 'F0000000000000',
          'id': 1000,
          'cups_id': [101, 'ES00000000000000000001']}], None  # To be updated


results = []
results.append(run_test(test_connection, 100))
results.append(run_test(test_users, 10))
results.append(run_test(test_contracts, 10))
results.append(run_test(test_billing, 10))

push_test('ERP status %s' % datetime.datetime.now(), results)
