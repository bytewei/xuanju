from django.db import models

class NaviClass(models.Model):
    name = models.CharField("网址分类", max_length=50, unique=True)
    remark = models.CharField("网址备注", max_length=200)

    class Meta:
        verbose_name = "网址分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Navi(models.Model):
    naviclass = models.ForeignKey(NaviClass, on_delete=models.CASCADE, verbose_name="网址分类")
    name = models.CharField("网址名称", max_length=50, unique=True)
    url = models.URLField("网址地址", unique=True)
    remark = models.CharField("网址备注", max_length=200)

    class Meta:
        verbose_name = "网址名称"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DocClass(models.Model):
    name = models.CharField("文档分类", max_length=50, unique=True)
    remark = models.CharField("分类备注", max_length=200)

    class Meta:
        verbose_name = "文档分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Doc(models.Model):
    docclass = models.ForeignKey(DocClass, on_delete=models.CASCADE, verbose_name="文档分类")
    name = models.CharField("文档名称", max_length=50, unique=True)
    url = models.URLField("文档地址", unique=True)
    remark = models.CharField("系统备注", max_length=200)

    class Meta:
        verbose_name = "文档名称"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
