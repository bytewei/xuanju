from django.contrib import admin
from .models import NaviClass, Navi, DocClass, Doc


class NaviClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'remark']
    search_fields = ['name', 'remark']
    list_filter = ['name', 'remark']


class NaviAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'remark']
    search_fields = ['name', 'url', 'remark']
    list_filter = ['name', 'url', 'remark']


class DocClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'remark']
    search_fields = ['name', 'remark']
    list_filter = ['name', 'remark']


class DocAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'remark']
    search_fields = ['name', 'url', 'remark']
    list_filter = ['name', 'url', 'remark']


admin.site.register(NaviClass, NaviClassAdmin)
admin.site.register(Navi, NaviAdmin)
admin.site.register(DocClass, DocClassAdmin)
admin.site.register(Doc, DocAdmin)
