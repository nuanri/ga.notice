import hashlib
import json

import requests
import requests_mock

from eva.conf import settings


MOCK_PARAM = {
    'result': True,
    'statusCode': 200,
    'message': 'mock 请求成功',
    'info': {'successCount': "mock 成功", 'smsIds': ['mock 成功']}
}

class SendCloudSms(object):
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def custom_vars(self):
        d = {}
        for k, v in self.data["template_args"].items():
            k = "%{}%".format(k)
            d[k] = v
        return d

    def custom_param(self):

        param = {
            "smsUser": settings.SMS_API_USER,
            "templateId": self.data["template_id"],
            "msgType": 0,
            "phone": self.data["phone"],
            "vars": json.dumps(self.custom_vars())
        }

        param_keys = list(param.keys())
        param_keys.sort()

        param_list = list(map(lambda key: "{0}={1}".format(key, param[key]), param_keys))

        sign_str = "{0}&{1}&{2}".format(
            settings.SMS_API_KEY,
            '&'.join(str(o) for o in param_list),
            settings.SMS_API_KEY
        )
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        param['signature'] = sign
        return param

    def send(self):
        with requests_mock.Mocker(real_http=True) as m:
            if settings.USE_MOCK:
                m.register_uri('POST', self.url, json=MOCK_PARAM)
            print(self.url, self.custom_param)
            res = requests.post(self.url, data=self.custom_param())
            print("res:", res.json())
            err = {}
            if res.json().get("statusCode") != 200:
                err["message"] = res.json().get("message")
                err["info"] = res.json().get("info")
            return err


class SendCloudEmail(object):
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def custom_vars(self):
        d = {}
        for k, v in self.data["template_args"].items():
            k = "%{}%".format(k)
            d[k] = [v]
        return d

    def custom_param(self):
        xsmtpapi = {
            'to': [self.data["email"]],
            'sub': self.custom_vars()
        }

        param = {
            "apiUser": settings.EMAIL_API_USER,  # 使用apiUser和apiKey进行验证
            "apiKey": settings.EMAIL_API_KEY,
            "templateInvokeName": self.data["template_name"],  # 模版名称
            "xsmtpapi": json.dumps(xsmtpapi),
            "from": settings.FROM_EMAIL,  # 发信人, 用正确邮件地址替代
            "fromName": settings.FROM_NAME,
            "subject": self.data["subject"]  # 邮件标题
        }
        return param

    def send(self):
        with requests_mock.Mocker(real_http=True) as m:
            if settings.USE_MOCK:
                m.register_uri('POST', self.url, json=MOCK_PARAM)
            res = requests.post(self.url, data=self.custom_param())
            print("res:", res.json())
            err = {}
            if res.json().get("statusCode") != 200:
                err["message"] = res.json().get("message")
                err["info"] = res.json().get("info")
            return err
