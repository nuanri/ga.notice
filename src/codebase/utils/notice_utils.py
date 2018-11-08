import hashlib
import json

import requests
import requests_mock

from eva.conf import settings


SMS_MOCK_PARAM = {
    'result': True,
    'statusCode': 200,
    'message': 'mock 请求成功',
    'info': {'successCount': "mock 成功", 'smsIds': ['mock 成功']}
}

EMAIL_MOCK_PARAM = {
    "result": "true",
    "statusCode": 200,
    "message": "mock 请求成功",
    "info": {"emailIdList": ["mock 成功"]}
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


def email_custom_param(**data):

    xsmtpapi = {
        'to': [data["email"]],
        'sub': {
            '%name%': [data["name"]],
            '%code%': [data["code"]],
        }
    }

    param = {
        "apiUser": settings.EMAIL_API_USER,  # 使用apiUser和apiKey进行验证
        "apiKey": settings.EMAIL_API_KEY,
        "templateInvokeName": settings.TEMPLATE_NAME,  # 模版名称
        "xsmtpapi": json.dumps(xsmtpapi),
        "from": settings.FROM_EMAIL,  # 发信人, 用正确邮件地址替代
        "fromName": settings.FROM_NAME,
        "subject": settings.EMAIL_SUBJECT  # 邮件标题
    }

    return param


def get_response(url, param, mock_param):
    with requests_mock.Mocker(real_http=True) as m:
        if settings.USE_MOCK:
            m.register_uri('POST', url, json=mock_param)
        res = requests.post(url, data=param)
    return res
