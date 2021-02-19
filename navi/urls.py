# file: urls.py
# author: renxiaowei
# date: 2020/9/29

from django.urls import path, include

from .views import NaviView, DocView

urlpatterns = [
    path('navi/', NaviView.as_view(), name='navi'),
    path('doc/', DocView.as_view(), name='doc'),
]
