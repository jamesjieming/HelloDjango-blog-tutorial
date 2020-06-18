
import markdown
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Post, Category, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import re


def index(request):
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 5))
    post_list = Post.objects.all()
    paginator = Paginator(post_list, per_page)
    page_object = paginator.page(page)
    # 分组页码
    page_ranges = [list(paginator.page_range)[i:i+5] for i in range(0, paginator.num_pages+1, 5)]
    page_range, next_page_range, before_page_range = [], [], []
    # 生成页码范围
    for i in range(0, len(page_ranges)):
        if page in page_ranges[i]:
            page_range = page_ranges[i]
            try:
                next_page_range = page_ranges[i+1]
            except IndexError:
                before_page_range = page_ranges[i-1]
                break
            if i == 0:
                break
            before_page_range = page_ranges[i-1]
            break
    data = {
        "page_object": page_object,
        "page_range": page_range,
        "next_page_range": next_page_range,
        "before_page_range": before_page_range,
        "post_list": post_list,
        "page_count": paginator.num_pages
    }
    return render(request, 'blog/index.html', context=data)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 原始markdown文档解析成html，启用md语法扩展
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',  # 基础扩展
        'markdown.extensions.codehilite',  # 语法高亮扩展
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


# 归档视图函数
def archive(request, year, month):
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 5))
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    paginator = Paginator(post_list, per_page)
    page_object = paginator.page(page)
    # 分组页码
    page_ranges = [list(paginator.page_range)[i:i+5] for i in range(0, paginator.num_pages+1, 5)]
    page_range, next_page_range, before_page_range = [], [], []
    # 生成页码范围
    for i in range(0, len(page_ranges)):
        if page in page_ranges[i]:
            page_range = page_ranges[i]
            try:
                next_page_range = page_ranges[i+1]
            except IndexError:
                before_page_range = page_ranges[i-1]
                break
            if i == 0:
                break
            before_page_range = page_ranges[i-1]
            break
    data = {
        "page_object": page_object,
        "page_range": page_range,
        "next_page_range": next_page_range,
        "before_page_range": before_page_range,
        "post_list": post_list,
        "page_count": paginator.num_pages
    }
    return render(request, 'blog/index.html', context=data)


def category(request, pk):
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 5))
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    paginator = Paginator(post_list, per_page)
    page_object = paginator.page(page)
    # 分组页码
    page_ranges = [list(paginator.page_range)[i:i + 5] for i in range(0, paginator.num_pages + 1, 5)]
    page_range, next_page_range, before_page_range = [], [], []
    # 生成页码范围
    for i in range(0, len(page_ranges)):
        if page in page_ranges[i]:
            page_range = page_ranges[i]
            try:
                next_page_range = page_ranges[i + 1]
            except IndexError:
                before_page_range = page_ranges[i - 1]
                break
            if i == 0:
                break
            before_page_range = page_ranges[i - 1]
            break
    data = {
        "page_object": page_object,
        "page_range": page_range,
        "next_page_range": next_page_range,
        "before_page_range": before_page_range,
        "post_list": post_list,
        "page_count": paginator.num_pages
    }
    return render(request, 'blog/index.html', context=data)


def tag(request, pk):
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 5))
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    paginator = Paginator(post_list, per_page)
    page_object = paginator.page(page)
    # 分组页码
    page_ranges = [list(paginator.page_range)[i:i + 5] for i in range(0, paginator.num_pages + 1, 5)]
    page_range, next_page_range, before_page_range = [], [], []
    # 生成页码范围
    for i in range(0, len(page_ranges)):
        if page in page_ranges[i]:
            page_range = page_ranges[i]
            try:
                next_page_range = page_ranges[i + 1]
            except IndexError:
                before_page_range = page_ranges[i - 1]
                break
            if i == 0:
                break
            before_page_range = page_ranges[i - 1]
            break
    data = {
        "page_object": page_object,
        "page_range": page_range,
        "next_page_range": next_page_range,
        "before_page_range": before_page_range,
        "post_list": post_list,
        "page_count": paginator.num_pages
    }
    return render(request, 'blog/index.html', context=data)


# Create your views here.


def full_width(request):

    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 2))
    post_list = Post.objects.all()
    paginator = Paginator(post_list, per_page)
    page_object = paginator.page(page)
    data = {
        "page_object": page_object,
        "page_range": paginator.page_range,
        "post_list": post_list,
        "page_count": paginator.num_pages
    }
    return render(request, 'blog/full-width.html', context=data)
