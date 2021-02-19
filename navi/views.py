from django.shortcuts import render

from django.views.generic import View
from .models import NaviClass, Navi, DocClass, Doc

from django.utils.safestring import mark_safe


# class Dashboard(View):
#     def get(self, request):
#         all_naviclass = NaviClass.objects.all()
#
#         naviclass = []
#         navidetail = []
#
#         for navicls in all_naviclass:
#             naviclass.append(navicls.name)
#             cls_num = len(navicls.navi_set.all())
#             cls_data = {"value": cls_num, "name": navicls.name}
#             navidetail.append(cls_data)
#
#         return render(request, 'navi/navi.html', {
#             'naviclass': naviclass,
#             'navidetail': navidetail,
#         })


# class AboutView(View):
#     def get(self, request):
#         return render(request, 'about.html')


class NaviView(View):
    def get(self, request):
        all_naviclass = NaviClass.objects.all()
        all_navi = Navi.objects.all()

        return render(request, 'navi/navi.html', {
            'all_naviclass': all_naviclass,
            'all_navi': all_navi,
        })


class DocView(View):
    def get(self, request):
        all_docclass = DocClass.objects.all()
        all_doc = Doc.objects.all()

        return render(request, 'navi/doc.html', {
            'all_docclass': all_docclass,
            'all_doc': all_doc,
        })
