from codebase.models import Notice
from codebase.utils.swaggerui import api

from .base import (
    BaseTestCase,
    get_body_json
)


class NoticeBaseTestCase(BaseTestCase):

    rs = api.spec.resources["notice"]


class SmsTestCase(NoticeBaseTestCase):
    """POST /sms - 发送手机验证码
    """

    def test_send_sms_success(self):
        """发送成功
        """
        resp = self.api_post("/sms", body={
            "phone": "66666666666",
            "text": {"code": "123456", "name": "abc"}
        })
        body = get_body_json(resp)

        self.assertEqual(resp.code, 200)
        self.validate_default_success(body)
        sms = self.db.query(Notice).filter_by(
            name="abc",
            code="123456",
            phone="66666666666"
        ).first()
        self.assertIsNot(sms, None)


class EmailTestCase(NoticeBaseTestCase):
    """POST /email - 发送邮件验证码
    """

    def test_send_email_success(self):
        """发送成功
        """
        resp = self.api_post("/email", body={
            "email": "**@**.com",
            "text": {"code": "123456", "name": "abc"}
        })
        body = get_body_json(resp)

        self.assertEqual(resp.code, 200)
        self.validate_default_success(body)
        notice = self.db.query(Notice).filter_by(
            name="abc",
            code="123456",
            email="**@**.com"
        ).first()
        self.assertIsNot(notice, None)
