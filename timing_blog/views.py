import markdown

from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from . import models
import pygments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse
from openai import Completion
import openai
import json
from django.http import JsonResponse

from django.shortcuts import redirect
from django_comments import models as comment_models
from django_comments.models import Comment

def wechat_login(request):
    # 生成微信登录链接
    wechat_login_url = 'https://open.weixin.qq.com/connect/qrconnect?appid=YOUR_APPID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect'
    return redirect(wechat_login_url)


def handle_question(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "")

        # 调用 ChatGPT 来生成答案
        openai.api_key = "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" # 替换为您的密钥
        completion = openai.Completion()
        response = completion.create(
            model="gpt-3.5-turbo",
            prompt=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=100,
            stop=["\n"]
        )

        # 返回答案给前端
        return JsonResponse({"answer": response.choices[0].text})
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

# 内置了一个分页的功能，导入分页的类，分页器，空页，不是整数页面的三个功能导入进来
# 从url找到视图，视图除了引出对应的页面，还要收录模型，才能显示信息。
# Create your views here.
def make_paginator(objects, page, num=6):
    # 写一个方法 自定义分页，对象的列表，查看第几页，每页显示几个
    paginator = Paginator(objects, num)
    # 生成提供分页工具的对象（分页器，5文一页），所有的博客，每页的数量
    try:
        # 获取当前的对象列表
        object_list = paginator.page(page)
    # 以下是一些异常的处理情况
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    return object_list, paginator


# 这段从github找到一个美观一点的分页器显示，不是重点，不难理解，简单但繁琐，多
# 就像前端一样，所以直接借鉴他人，拿来主义，直接就是拿来用就行了
def pagination_data(paginator, page):
    """
    用于自定义展示分页页码的方法
    :param paginator: Paginator类的对象
    :param page: 当前请求的页码
    :return: 一个包含所有页码和符号的字典
    """
    if paginator.num_pages == 1:
        # 如果无法分页，也就是只有1页不到的内容，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
        return {}
    # 当前页左边连续的页码号，初始值为空
    left = []

    # 当前页右边连续的页码号，初始值为空
    right = []

    # 标示第 1 页页码后是否需要显示省略号
    left_has_more = False

    # 标示最后一页页码前是否需要显示省略号
    right_has_more = False

    # 标示是否需要显示第 1 页的页码号。
    # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
    # 其它情况下第一页的页码是始终需要显示的。
    # 初始值为 False
    first = False

    # 标示是否需要显示最后一页的页码号。
    # 需要此指示变量的理由和上面相同。
    last = False

    # 获得用户当前请求的页码号
    try:
        page_number = int(page)
    except ValueError:
        page_number = 1
    except:
        page_number = 1

    # 获得分页后的总页数
    total_pages = paginator.num_pages

    # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
    page_range = paginator.page_range

    if page_number == 1:
        # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
        # 此时只要获取当前页右边的连续页码号，
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
        # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        right = page_range[page_number:page_number + 4]

        # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
        # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
        if right[-1] < total_pages - 1:
            right_has_more = True

        # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
        # 所以需要显示最后一页的页码号，通过 last 来指示
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
        # 此时只要获取当前页左边的连续页码号。
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
        # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        # 如果最左边的页码号比第 2 页页码号还大，
        # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
        if left[0] > 2:
            left_has_more = True

        # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
        # 所以需要显示第一页的页码号，通过 first 来指示
        if left[0] > 1:
            first = True
    else:
        # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
        # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        # 是否需要显示最后一页和最后一页前的省略号
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        # 是否需要显示第 1 页和第 1 页后的省略号
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
    }
    return data


def index(request):
    entries = models.Entry.objects.all()
    #     把模型的所有文章都导进来
    page = request.GET.get('page', 1)
    # 从request的GET方法里获取page的值
    entry_list, paginator = make_paginator(entries, page)
    # 这个entry-list就是选择当前页的数量有哪几个，就是类似于主函数调用自定义函数
    page_data = pagination_data(paginator, page)
    # 生成美化版的分页标签，方法借鉴别人的写在了上面的自定义函数里面
    return render(request, 'timing_blog/index.html', locals())


'''渲染第一个参数为request，
第二个视图文件视图放在timing_blog下面的index点HTML。
然后给个locals，把当前所有的变量全部打到那个打包成字典传进去，、
在timing_blog下面创建一个目录，叫做template，
在templates下面再创建个目录，叫做timing_blog
'''


def detail(request, blog_id):
    # entry = models.Entry.objects.get(id=blog_id)
    entry = get_object_or_404(models.Entry, id=blog_id)
    # 把某篇具体的文章导进来，然后就会执行增加的方法
    md = markdown.Markdown(extensions=[
        # 类，这个参数是个列表，提供一些语法内容
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 高亮
        'markdown.extensions.toc',
    ])
    # 定义了一个md，让文章的body转化成这个新的格式
    entry.body = md.convert(entry.body)
    entry.toc = md.toc
    # 列表，目录
    entry.increase_visiting()
    comment_list = list()

    def get_comment_list(comments):
        for comment in comments:
            comment_list.append(comment)
            children = comment.child_comment.all()
            if len(children) > 0:
                get_comment_list(children)

    top_comments = Comment.objects.filter(object_pk=blog_id, parent_comment=None,
                                          content_type__app_label='timing_blog').order_by('-submit_date')

    get_comment_list(top_comments)
    return render(request, 'timing_blog/detail.html', locals())


def category(request, category_id):
    # c = models.Category.objects.get(id=category_id)
    # 获取分类ID传过来的参数的对象。
    c = get_object_or_404(models.Category, id=category_id)
    # 确保传过来的参数不会出问题，出问题我就404
    entries = models.Entry.objects.filter(category=c)
    # 过滤器，这个分类下有哪些博客
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'timing_blog/index.html', locals())


def tag(request, tag_id):
    # t = models.Tag.objects.get(id=tag_id)
    t = get_object_or_404(models.Tag, id=tag_id)
    # 如上，目录和细节，这个是标签
    if t.name == "全部":
        entries = models.Entry.objects.all()
    else:
        entries = models.Entry.objects.filter(tags=t)

    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'timing_blog/index.html', locals())


def search(request):
    keyword = request.GET.get('keyword', None)
    # 获取关键字，如果没有那就是none
    if not keyword:
        error_msg = "请输入关键字"
        # 如果没有关键字，打印一个错误
        return render(request, 'timing_blog/index.html', locals())
    # 如果有关键字，那就搜索内容
    entries = models.Entry.objects.filter(Q(title__icontains=keyword)
                                          | Q(body__icontains=keyword)
                                          | Q(abstract__icontains=keyword))
    # Q搜索，Q函数，是专门用于搜索的，django内置提供的过滤函数。

    page = request.GET.get('page', 1)
    # 默认开始显示页数
    entry_list, paginator = make_paginator(entries, page)
    # 分页器，每页显示什么东西
    page_data = pagination_data(paginator, page)
    # 美化过的页数选择框
    return render(request, 'timing_blog/index.html', locals())


def archives(request, year, month):
    entries = models.Entry.objects.filter(created_time__year=year, created_time__month=month)
    # 类，形参导入数据变成实参，导进变量对象
    # 过滤器，这个分类下有哪些博客
    page = request.GET.get('page', 1)
    entry_list, paginator = make_paginator(entries, page)
    page_data = pagination_data(paginator, page)
    return render(request, 'timing_blog/index.html', locals())


def permission_denied(request, exception):
    return render(request, 'timing_blog/403.html', locals())


def page_not_found(request, exception):
    return render(request, 'timing_blog/404.html', locals())


def page_error(request):
    return render(request, 'timing_blog/500.html', locals())
def reply(request, comment_id):
    # if not request.session.get('login', None) and not request.user.is_authenticated():
    #     return redirect('/')
    # 让它不登陆也能回复
    parent_comment = get_object_or_404(comment_models.Comment, id=comment_id)
    return render(request, 'timing_blog/reply.html', locals())
