"""
URL configuration for dj_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('timing_blog/', include('timing_blog.urls'))
"""
# 设计路由视图和模板，这里是根目录路由
from django.contrib import admin
from django.urls import path, re_path

''' 想在 Django 项目中配置处理 URL，
应该使用 Django 提供的内置模块（包），函数/方法（文件/类）
`django.conf.urls.url` 是 Django 1.x 版本中的 URL 配置方法，
但在 Django 2.x 及更新版本中，推荐使用 `django.urls.re_path`
 或 `django.urls.path` 进行 URL 配置。
'''

from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from timing_blog.feed import LatestEntriesFeed
from timing_blog import views as blog_views

'''
 是用于包含其他 URL 配置的常用模块。
 它是 Django 中的标准功能，通常不会与特定环境或版本不兼容。
 在Django 2.x及更高版本中，`include` 函数已经被移动到 `django.urls` 模块中，
 所以如果你已经导入了 `from django.urls import path`，
 通常情况下就不需要再导入 `from django.conf.urls import include`。
'''

# 快捷方式快速生成网络地图，不需要给站点地图单独写视图模块
# 直接在URLconfer里面获取对象，然后传递参数设置URL，
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from timing_blog.models import Entry
info_dict = {
    # 生成一个字典，查询集，是所有博客都要放进来站点里面
    'queryset': Entry.objects.all(),
    'date_field': 'modified_time'
}
from timing_blog import views
urlpatterns = [
                  re_path(r'^$', blog_views.index),
                  re_path(r'^admin/', admin.site.urls),
                  re_path(r'^timing_blog/', include('timing_blog.urls')),
                  #     每个以timing_blog开头的路由都把它转发到timing_blog下面的urls
                  # 定义 URL 二级路由
                  re_path(r'^latest/feed/$', LatestEntriesFeed()),
                  re_path(r'^comments/', include('django_comments.urls')),
                  # 凡是走comments的URL都转发到django_comments.urls里面
                  re_path(r'^sitemap\.xml$', sitemap,{'sitemaps':{'timing_blog':GenericSitemap(info_dict,priority=0.6)}},name='django.contrib.sitemaps.views.sitemap'),
                  re_path(r'^qa/', views.handle_question, name='handle_question'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 设定图片的URL找到图片内容，类似于下面的这个
# re_path(r'^(?P<blog_id>[0-9]+)', views.detail, name='blog_detail'),
handler403 = blog_views.permission_denied
# 403禁止访问，权限不允许  ，写个视图专门处理这个
handler404 = blog_views.page_not_found
# 404页面不存在，
handler500 = blog_views.page_error
# 500服务器错误
