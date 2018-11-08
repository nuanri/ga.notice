# pylint: disable=W0223,W0221,broad-except

from codebase.web import APIRequestHandler
from codebase.models import Notice
from eva.conf import settings
from codebase.utils.notice_utils import (
    get_response,
    sms_custom_param,
    SMS_MOCK_PARAM,
    email_custom_param,
    EMAIL_MOCK_PARAM,
)


class SmsHandler(APIRequestHandler):

    def post(self):
        """发送手机验证码
        """
        body = self.get_body_json()

        data = {
            "phone": body["phone"],
            "name": body["text"]["name"],
            "code": body["text"]["code"]
        }

        param = sms_custom_param(**data)
        res = get_response(settings.SMS_URL, param, SMS_MOCK_PARAM)

        if res.json().get("statusCode") != 200:
            err = {}
            err["message"] = res.json().get("message")
            err["info"] = res.json().get("info")

            self.fail(err)
            return

        notice = Notice(
            name=body["text"]["name"],
            code=body["text"]["code"],
            phone=body["phone"],
        )
        self.db.add(notice)
        self.db.commit()
        self.success()


class EmailHandler(APIRequestHandler):

    def post(self):

        body = self.get_body_json()

        data = {
            "email": body["email"],
            "name": body["text"]["name"],
            "code": body["text"]["code"]
        }
        param = email_custom_param(**data)
        res = get_response(settings.EMAIL_URL, param, EMAIL_MOCK_PARAM)

        if res.json().get("statusCode") != 200:
            err = {}
            err["message"] = res.json().get("message")
            err["info"] = res.json().get("info")

            self.fail(err)
            return

        notice = Notice(
            name=body["text"]["name"],
            code=body["text"]["code"],
            email=body["email"],
        )
        self.db.add(notice)
        self.db.commit()
        self.success()
