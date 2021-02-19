# file: forms.py
# author: renxiaowei
# date: 2020/10/9

from captcha.fields import CaptchaField
from python_freeipa import ClientMeta

from django import forms
from xuanju.settings import IPA_AUTH_SERVER, IPA_AUTH_USER, IPA_AUTH_PWD


class LoginUserForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True,min_length=3, max_length=100)
    captcha = CaptchaField()

    def clean_email(self):
        email = self.data.get("email")
        if email.endswith("@cnstrong.cn"):
            user = email.split("@")[0]
            client = ClientMeta(host=IPA_AUTH_SERVER, verify_ssl=False)
            client.login(IPA_AUTH_USER, IPA_AUTH_PWD)
            account = client.user_find(user)
            if account:
                print("account is:", account)
            else:
                print("No user: ", account)
                raise forms.ValidationError('无效的LDAP账号')
        else:
            print("no right mail:", email)
            raise forms.ValidationError('非公司邮箱')
        return email


class ChangePwdForm(forms.Form):
    user = forms.CharField(required=True)
    current_password = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)

    def clean(self):
        user = self.cleaned_data["user"]
        current_pwd = self.cleaned_data["current_password"]
        pwd1 = self.cleaned_data["password"]
        pwd2 = self.cleaned_data["password2"]

        if not current_pwd and not user:
            raise forms.ValidationError("当前密码为空")

        if pwd1 != pwd2:
            raise forms.ValidationError("两次输入密码不一致")

        return self.cleaned_data


class GeneratePwdForm(forms.Form):
    number = forms.CharField(required=True)
