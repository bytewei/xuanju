from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers

from .forms import LoginUserForm, ForgetForm, ChangePwdForm, GeneratePwdForm
from .models import EmailVerifyRecord

from utils.email_send import send_register_email, change_ldap_pwd, random_pwd

from datetime import datetime, timedelta


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        next = request.GET.get("next", "")
        login_form = LoginUserForm()
        return render(request, 'users/login.html', {"login_form": login_form,
                                                    "next": next})

    def post(self, request, *args, **kwargs):
        login_form = LoginUserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "users/login.html", {"msg": "密码错误或密码已过期，请考虑设置新密码（'忘记密码'）",
                                                            "login_form": login_form})
        else:
            return render(request, "users/login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'users/forget.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            print('forget_form is:', forget_form)
            time = datetime.now() - timedelta(days=1)

            # get user ip
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.META.get("REMOTE_ADDR")

            result = EmailVerifyRecord.objects.filter(send_time__gt=time, user_ip=ip)
            if (len(result) < 600 or len(result) == 0):
                email = forget_form.cleaned_data["email"]
                send = send_register_email(email, send_type='forget', user_ip=ip)
                if send:
                    print('send mail success.')
                    print('send status: ', send)
                    return render(request, 'users/success_send.html', {'email': email})
                else:
                    print('send mail fail.')
                    print('send status: ', send)
                    return render(request, 'users/fault_reset.html', {'msg': '邮件发送过程中遇到错误，请再试一次.'})
            else:
                return render(request, 'users/fault_reset.html', {'msg': '一天只能设置6次密码，请明天重试.'})


class ResetView(View):
    '''重置密码get部分'''
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.filter(code=active_code)
        if record:
            # add expire time for link
            for i in record:
                email = i.email
                if ( email and i.is_use == 'no' ):
                    # 获取并格式化当前时间
                    now_time = datetime.now().strftime('%Y%m%d %H%M%S')
                    # 获取并格式化邮件过期时间
                    expire_time = i.expire_time.strftime('%Y%m%d %H%M%S')
                    if now_time < expire_time:
                        i.is_use = 'yes'
                        i.save()
                        return render(request, 'users/email_check.html', {'email': email})
                    return render(request, 'users/fault_reset.html', {'msg': "激活时间已过期，请重新设置密码",
                                                                      'email': email})
                return render(request, 'users/fault_reset.html', {'msg': "激活链接已使用，请重新设置密码",
                                                                  'email': email})
        return render(request, 'users/fault_reset.html', {'msg': "未找到激活码，请确认邮件内容"})


class ModifyView(View):
    '''重置密码post部分'''
    def post(self, request, *args, **kwargs):
            email = request.POST.get('email', '')
            if email:
                user = email.split("@")[0]
                password = send_register_email(email, send_type='reset_result', user=user)
                if password:
                    return render(request, 'users/success_reset.html', {
                        'user': user,
                        'password': password,
                        'email': email
                    })
            return render(request, 'users/email_check.html', {'email': email})


class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/users/login/"
    def get(self, request):
        pwd_form = ChangePwdForm()
        return render(request, 'users/pwd_change.html', {'pwd_from': pwd_form})

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            current_password = request.POST.get("current_password", "")
            password = request.POST.get("password", "")
            user = request.POST.get("user", "")
            print("user is: ", user)
            change_password = change_ldap_pwd(user=user, current_password=current_password, password=password)
            if change_password:
                return render(request, 'users/pwd_change_success.html', {'user': user })
            else:
                print("change password failed")
                return render(request, 'users/pwd_change_fault.html', {'msg': "密码修改失败"})
        else:
            print("密码输入不匹配")
            return render(request, 'users/pwd_change_fault.html', {'msg': "密码输入不匹配"})


class GeneratePwdView(LoginRequiredMixin, View):
    login_url = "/users/login/"
    def get(self, request):
        return render(request, 'users/pwd_tool.html')

    def post(self, request, *args, **kwargs):
        generate_form = GeneratePwdForm(request.POST)
        if generate_form.is_valid():
            num_str = request.POST.get("number", "")
            number = int(num_str)
            if number < 12:
                random_password = random_pwd(randomlength=number)
            elif number < 15:
                random_password = random_pwd(randomlength=number, digits=3, upper=4, lower=4)
            elif number < 18:
                random_password = random_pwd(randomlength=number, digits=4, upper=5, lower=5)
            else:
                random_password = random_pwd(randomlength=number, digits=5, upper=6, lower=6)
            return render(request, 'users/pwd_tool.html', {'random_password': random_password, 'number': number})
