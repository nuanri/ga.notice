# pylint: disable=W0223,W0221,broad-except
import json

from tornado.web import HTTPError

from codebase.web import APIRequestHandler
from codebase.models import Notice
from eva.conf import settings
from codebase.utils.sendcloud import (
    SendCloudSms,
    SendCloudEmail
)




class _BaseNoticeRoleHandler(APIRequestHandler):

    def get_uid(self):
        uid = self.request.headers.get("X-User-Id")
        if not uid:
            raise HTTPError(403, reason="no-x-user-id")
        return uid

    def validate_data(self):
        body = self.get_body_json()
        for k, v in body["template_args"].items():
            if not isinstance(k, str):
                self.fail("字典 key 类型错误")
                return False
            if not isinstance(v, (int, str)):
                self.fail("字典 value 类型错误")
                return False
        return True


class SmsHandler(_BaseNoticeRoleHandler):

    def post(self):
        """发送手机验证码
        """
        if not self.validate_data():
            return

        body = self.get_body_json()

        sendcloud = SendCloudSms(settings.SMS_URL, body)
        err = sendcloud.send()
        if err:
            self.fail(err)
            return

        notice = Notice(
            phone=body["phone"],
            template_id=int(body["template_id"]),
            template_args=json.dumps(body["template_args"]),
            uid=self.get_uid(),
            type="sms"
        )
        self.db.add(notice)
        self.db.commit()
        self.success()


class EmailHandler(_BaseNoticeRoleHandler):

    def post(self):
        '''发送邮箱验证码
        '''
        if not self.validate_data():
            return

        body = self.get_body_json()

        sendcloud = SendCloudEmail(settings.EMAIL_URL, body)
        err = sendcloud.send()
        if err:
            self.fail(err)
            return

        notice = Notice(
            template_name=body["template_name"],
            template_args=json.dumps(body["template_args"]),
            email=body["email"],
            uid=self.get_uid(),
            type="email"
        )
        self.db.add(notice)
        self.db.commit()
        self.success()
