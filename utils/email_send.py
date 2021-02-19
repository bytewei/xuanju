# file: email_send.py
# author: renxiaowei
# date: 2020/10/10

import string
from itertools import chain
from random import choice, sample
from random import Random
from python_freeipa import ClientMeta

from users.models import EmailVerifyRecord

from django.core.mail import send_mail
from xuanju.settings import EMAIL_FROM
from xuanju.settings import IPA_AUTH_SERVER, IPA_AUTH_USER, IPA_AUTH_PWD

from subprocess import Popen, PIPE
from datetime import datetime, timedelta


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()

    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def random_pwd(randomlength=10, digits=3, upper=3, lower=3):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    salt = '!@#$%^&*'

    password = list(
        chain(
            (choice(uppercase) for _ in range(upper)),
            (choice(lowercase) for _ in range(lower)),
            (choice(string.digits) for _ in range(digits)),
            (choice(salt) for _ in range((randomlength - digits - upper - lower)))
        )
    )
    return "".join(sample(password, len(password)))


def reset_ldap_pwd(user):
    user = user
    client = ClientMeta(host=IPA_AUTH_SERVER, verify_ssl=False)
    client.login(IPA_AUTH_USER, IPA_AUTH_PWD)
    password = client.user_mod(user, o_random=True)['result']['randompassword']
    if password:
        days = timedelta(days=1)
        expire_time = datetime.now() + days
        str_expire = expire_time.strftime('%Y%m%d%H%M%S') + 'Z'
        change_expire = client.user_mod(user, o_krbpasswordexpiration=str_expire)
        if change_expire:
            return password
        else:
            print("Change krbpasswordexpiration failed.")
            return 0
    else:
        print("Set password failed.")
        return 0

def change_ldap_pwd(user, current_password, password):
    user = user
    client = ClientMeta(host=IPA_AUTH_SERVER, verify_ssl=False)
    client.login(IPA_AUTH_USER, IPA_AUTH_PWD)
    change_pwd = client.passwd(a_principal=user, a_current_password=current_password, a_password=password)
    if change_pwd:
        days = timedelta(days=180)
        expire_time = datetime.now() + days
        str_expire = expire_time.strftime('%Y%m%d%H%M%S') + 'Z'
        change_expire = client.user_mod(user, o_krbpasswordexpiration=str_expire)
        if change_expire:
            return 1
        else:
            raise exception_class(message, code)
            # return 0
    else:
        print("Change password failed.")
        return 0


def send_register_email(email, send_type='forget', user_ip='user_ip', user='user'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    if send_type == 'forget':
        hours = 2
        time = timedelta(hours=hours)
        email_record.expire_time = datetime.now() + time
        email_record.user_ip = user_ip
        email_record.save()
        email_title = 'Ops公司内网-导航 忘记密码 重置链接'
        email_body = '忘记密码?\r\n请在{0}小时内点击下面的链接设置你的新密码：http://127.0.0.1:8000/users/reset/{1}'.format(hours, code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return 1
        else:
            return 0

    elif send_type == 'reset_result':
        password = reset_ldap_pwd(user=user)
        email_title = 'Ops公司内网-导航 重置密码成功'
        email_body = '您好，下面是重置密码结果：\r\n LDAP账号：{0}\r\n LDAP密码：{1}\r\n 请在24小时内修改该密码，否则将过期无法使用。'.format(user, password)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return password

    elif send_type == 'login':
        pass
