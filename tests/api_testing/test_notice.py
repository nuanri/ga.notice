from eva.utils.time_ import utc_rfc3339_string

from codebase.models import Sms
from codebase.utils.sqlalchemy import dbc
from codebase.utils.swaggerui import api
from eva.conf import settings

from .base import (
    BaseTestCase,
    validate_default_error,
    get_body_json
)


class NoticeBaseTestCase(BaseTestCase):

    rs = api.spec.resources["notice"]


class SmsTestCase(NoticeBaseTestCase):
    """POST /sms - 发送手机验证码
    """

    def test_create_success(self):
        """创建成功
        """
        resp = self.api_post("/sms", body={
            "phone": "66666666666",
            "text": {"code": "123456", "name": "abc"}
        })
        body = get_body_json(resp)

        self.assertEqual(resp.code, 200)
        self.validate_default_success(body)
        sms = self.db.query(Sms).filter_by(
            name="abc",
            code="123456",
            phone="66666666666"
        ).first()
        self.assertIsNot(sms, None)
