from django.contrib.syndication.views import Feed
# from django.urls import reverse
from .models import Entry
#导入文章
# RSS订阅 方便自动推送文章 内置了一个高层次聚合内容的框架 让此功能变简单，只需要创建一个简单的类去调用接口即可，官网例子那过来
class LatestEntriesFeed(Feed):
    # 最近的博客
    title = "澍时的博客网站"
    link = "/siteblogs/"
    description = "最新更新的博客文章！"

    def items(self):
        return Entry.objects.order_by('-created_time')[:5]
    # 获取逆序的5个最新博客
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract

    # item_link is only needed if entries has no get_absolute_url method.
    # def item_link(self, item):
    #     return reverse('news-item', args=[item.pk])

