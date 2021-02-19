from django.db import models
from datetime import datetime

class EmailVerifyRecord(models.Model):
    '''邮箱验证码'''
    use_choice = (
        ("yes", "已使用"),
        ("no", "未使用"),
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    user_ip = models.CharField('用户IP', max_length=15, default='0.0.0.0')
    send_type = models.CharField('验证码类型', choices=(('forget', '忘记密码'), ('login', '登陆')), max_length=20)
    send_time = models.DateTimeField('发送时间', default=datetime.now)
    expire_time = models.DateTimeField('过期时间', default=datetime.now)
    is_use = models.CharField('是否使用', choices=use_choice, default="no", max_length=3)


    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0} ({1})'.format(self.code, self.email)
