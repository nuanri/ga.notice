DEBUG = True
SYNC_DATABASE = True

SECRET_KEY = "IpVDzxWOPQP9xxONJYdUHK1PNcyt4182Zulua6xfWkvZgp"

# http://docs.sqlalchemy.org/en/latest/core/engines.html
DB_URI = "sqlite://"

PAGE_SIZE = 10

# 可以自定义任何变量
ADMIN_ROLE_NAME = "admin"

# sendcloud 相关配置
SMS_USER = ""
SMS_KEY = ""
SMS_URL = "http://www.sendcloud.net/smsapi/send"
TEMPLATE_ID = 21325

# USE_MOCK 为 True 时为使用 mock，为 False 时不使用 mock
USE_MOCK = False
