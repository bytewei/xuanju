# file: urls.py
# author: renxiaowei
# date: 2020/9/30

from django.urls import path
from .views import LoginView, LogoutView, ForgetPwdView, ResetView, ModifyView, ChangePwdView, GeneratePwdView

app_name='users'
urlpatterns = [
    # login
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # 忘记密码
    path('forget/', ForgetPwdView.as_view(), name='forget'),
    # 重置密码
    path('reset/<str:active_code>', ResetView.as_view(), name='reset'),
    path('modify/', ModifyView.as_view(), name='modify'),
    # 修改密码
    path('change/', ChangePwdView.as_view(), name='change'),
    # 密码生成工具
    path('generate/', GeneratePwdView.as_view(), name='generate'),
]
