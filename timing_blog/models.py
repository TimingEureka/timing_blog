from django.contrib.auth.models import User
# 库里的user方法
from django.db import models
from django.urls import reverse


# 内置模块（包、库），文件/类()，函数/方法def，变量/对象

# 模型、组成（变量，对象）、约束（参数）、指向、别名、回组、元类

# Create your models here.
class Category(models.Model):  # 类别
    # 自建模型
    name = models.CharField(max_length=128, verbose_name='博客分类')

    # 组成模型的字段 和 对应的约束条件/指向模型，别名

    def __str__(self):
        return self.name  # 打印名字而非生硬的对象

    class Meta:  # 元类、属性字段
        verbose_name = "博客分类"
        verbose_name_plural = '博客分类'  # 复数接轨


class Tag(models.Model):
    name = models.CharField(max_length=128, verbose_name='博客标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客标签"
        verbose_name_plural = '博客标签'


class Entry(models.Model):
    title = models.CharField(max_length=128, verbose_name='文章标题')

    author = models.ForeignKey(User, verbose_name='博客作者', on_delete=models.CASCADE)
    # 外键，主键，用户模型，直接使用内置的user模型
    img = models.ImageField(upload_to='blog_images', null=True, blank=True, verbose_name='博客配图')

    body = models.TextField(verbose_name='博客正文')

    abstract = models.TextField(max_length=256, blank=True, null=True, verbose_name='博客摘要')

    visiting = models.PositiveIntegerField(default=0, verbose_name='博客访问量')
    # 正整数，刚开始为0
    category = models.ManyToManyField('Category', verbose_name='博客分类')

    tags = models.ManyToManyField('Tag', verbose_name='博客标签')
    # 多对多的关系模型
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # 修改时间

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('timing_blog:blog_detail', kwargs={'blog_id': self.id})

    # 生成某一篇博客的URL绝对路径  参数通过字典键获取，为解析提供参数生成完整的url
    def increase_visiting(self):
        self.visiting += 1
        self.save(update_fields=['visiting'])

    # 保存点击量的数据并显示，指定保存字段
    class Meta:
        ordering = ['-created_time']
        # 获取博客数据，写这段方便排序，且自定义评论中也需要。
        # 学会习惯给需要查询的对象添加一个默认排序值。不添加ID会有问题，一旦碰到就麻烦
        verbose_name = "博客"
        verbose_name_plural = '博客'
