
# 公司内网导航系统

![](https://img.shields.io/badge/build-release-brightgreen.svg)  
![](https://img.shields.io/badge/version-v1.0.0-brightgreen.svg)  
![](https://img.shields.io/badge/python-3.7-brightgreen.svg)
![](https://img.shields.io/badge/Django-2.2-brightgreen.svg)


## 功能简介

- 说明
    - 本系统在我原有基础上删减、修改后开源，里面涉及的网址、密码等信息均已修改，请使用的同学自行修改为自己的。

- 系统定位
    - 公司各子系统网址导航
    - 重要文档链接导航
    - OpenLDAP账号密码自助修改、找回（基于freeIPA api实现）
    
- 用户管理
    - 用户可使用LDAP账号登录该导航系统测试LDAP账号是否可用，进而直接使用LDAP账号登录其他系统。

- 通知
    - E-mail邮件推送，通知LDAP找回的密码


## 环境

- Python 3.7
    - Django 2.2
    
- Gentelella
    - Bootstrap4，用于前端页面展示

- SimpleUI
    - Django后台，用于替换原生admin系统

- DB
    - MySQL5.7
    

## 界面展示

- 邮件提醒

![image](https://github.com/wellfulren/xx/mail.png)

