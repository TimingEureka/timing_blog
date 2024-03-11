from django import template
from ..models import Entry,Category,Tag

register = template.Library()
# 生成一个注册器对象，用这个库，这个语法比较新

@register.simple_tag
# 这个函数就成了自定义模板标签，装饰器，不要执行，注册成
def get_recent_entries(num=5):
    # 最近5个，
    return Entry.objects.all().order_by('-created_time')[:num]
# 排序通过时间来倒叙，最新的5个博客

@register.simple_tag
def get_popular_entries(num=5):
    return Entry.objects.all().order_by('-visiting')[:num]
# 访问量最多的5篇文章

@register.simple_tag
def get_categories():
    return Category.objects.all()
# 博客分类

@register.simple_tag
def get_entry_count_of_category(category_name):
    return Entry.objects.filter(category__name=category_name).count()
# 获取博客分类数量

@register.simple_tag
def archives():
    # 根据博客发表的时间，进行排序和搜索，从而归档我们的博客
    return Entry.objects.dates('created_time', 'month', order='DESC')
# 降序排序，获取archives

@register.simple_tag
def get_entry_count_of_date(year, month):
    return Entry.objects.filter(created_time__year=year, created_time__month=month).count()
# 获取某个时间段下的博客总数,变量，与 形参

@register.simple_tag
def get_tags():
    return Tag.objects.all()