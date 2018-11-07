# pylint: disable=W0223,W0221,broad-except

from codebase.web import APIRequestHandler
from codebase.models import Sms
from eva.conf import settings
from codebase.utils.notice_utils import (
    get_response,
    sms_custom_param,
    SMS_MOCK_PARAM,
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

        sms = Sms(
            name=body["text"]["name"],
            code=body["text"]["code"],
            phone=body["phone"],
        )
        self.db.add(sms)
        self.db.commit()
        self.success()
