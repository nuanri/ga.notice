import hashlib
import json

import requests
import requests_mock

from eva.conf import settings


SMS_MOCK_PARAM = {
    'result': True,
    'statusCode': 200,
    'message': 'mock请求成功',
    'info': {'successCount': "mock成功", 'smsIds': ['mock成功']}
    }


def sms_custom_param(**data):

    param = {
        "smsUser": settings.SMS_USER,
        "templateId": settings.TEMPLATE_ID,
        "msgType": 0,
        "phone": data["phone"],
        "vars": json.dumps({"%name%": data["name"], "%code%": data["code"]})
    }

    param_keys = list(param.keys())
    param_keys.sort()

    param_list = list(map(lambda key: "{0}={1}".format(key, param[key]), param_keys))

    sign_str = "{0}&{1}&{2}".format(
        settings.SMS_KEY,
        '&'.join(str(o) for o in param_list),
        settings.SMS_KEY
    )
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    param['signature'] = sign

    return param


def get_response(url, param, mock_param):
    with requests_mock.Mocker(real_http=True) as m:
        if settings.USE_MOCK:
            m.register_uri('POST', url, json=mock_param)
        res = requests.post(url, data=param)
    return res
