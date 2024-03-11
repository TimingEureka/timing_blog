# 设计路由视图和模板，这里是二级目录路由
from django.urls import path, re_path
''' 
想在 Django 项目中配置处理 URL，
应该使用 Django 提供的内置模块（包），函数/方法，文件/类
`django.conf.urls.url` 是 Django 1.x 版本中的 URL 配置方法，
但在 Django 2.x 及更新版本中，推荐使用 `django.urls.re_path`
 或 `django.urls.path` 进行 URL 配置。
'''
from . import views

app_name = 'timing_blog'
urlpatterns = [
    re_path(r'^$', views.index, name='blog_index'),
    # 代表域名后面什么都没有
    re_path(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='blog_detail'),
    # 详情页，接受一个数字作为参数，命名为 blog_id,给每篇文章detail设计好了一个url
    re_path(r'^category/(?P<category_id>[0-9]+)/$', views.category, name='blog_category'),
    re_path(r'^tag/(?P<tag_id>[0-9]+)/$', views.tag, name='blog_tag'),
    re_path(r'^search/$', views.search, name='blog_search'),
    re_path(r'^archives/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', views.archives, name='blog_archives'),
    re_path(r'^qa/', views.handle_question, name='handle_question'),
    re_path(r'^wechat_login/', views.wechat_login, name='wechat_login'),
    re_path(r'^reply/(?P<comment_id>\d+)/$', views.reply, name='comment_reply'),

]

# 定义 URL 二级路由
'''
 $表示什么都没有，空，直接就是表示查看首页，并提供一个路由反向查询名
    都是为了让我们这个blog能够独立出来。
能够成为一个隔离的环境，不会跟其他的APP冲突，
以后也要使用这种技巧，看起来麻烦，但实际上受益无穷，
尤其是项目很大的时候。所以建议在这写一个APP name。
这就是给这个博客提供一个命名空空间，
以后所有的路由它的名字都以这个开头，
防止APP它之间URL反向解析，有可能会重名
其实这里name='blog_index可以不用前缀，但是填上去更显眼
'''
