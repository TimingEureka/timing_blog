from django.contrib import admin
from . import models


# Register your models here.
# 把models导入进来


class EntryAdmin(admin.ModelAdmin):
    # 定制显示方式，一个列表，指向组成字段
    list_display = ['title', 'author', 'visiting', 'created_time', 'modified_time']


# 注册（显示）各个模型字段
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Entry, EntryAdmin)
