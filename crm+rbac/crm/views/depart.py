from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from crm.utils.pager import Pagination
from crm.forms.my_form import DepartModelForm
from crm.utils.url import rev_url
from django.db.models import Q


def depart_list(request):
    # 当前页
    page = int(request.GET.get('page', 1))
    # 数据总条数
    total_num = models.Department.objects.all().count()
    # 每页显示的数据条数
    per_num = 10
    # 总页码数
    total_page_num, more = divmod(total_num, per_num)
    if more:
        total_page_num += 1
    # 最多显示页码数
    max_show = 11
    half_show = max_show // 2
    # 获取所有的数据
    """

    第1页 ： 0   10
    第2页 ： 10   20
    第n页： (n-1)*10 n*10  
    :param request:
    :return:
    """
    page_start = page - half_show  # 1
    page_end = page + half_show  # 11

    # 数据量少，不够生成11个页面的时候
    if total_page_num < max_show:
        page_start = 1
        page_end = total_page_num
    else:
        # 可以生成11个页码
        #  1 2 3 4 5
        if page <= half_show:
            page_start = 1
            page_end = max_show
        elif page + half_show > total_page_num:
            page_start = total_page_num - max_show + 1
            page_end = total_page_num
        else:
            page_start = page - half_show
            page_end = page + half_show

    page_list = []
    if page == 1:
        page_list.append('<li class="disabled"> <span aria-hidden="true">&laquo;</span>  </li>')
    else:
        page_list.append('<li><a href="/crm/depart/list/?page={}">&laquo;</a></li>'.format(page - 1))

    for i in range(page_start, page_end + 1):
        if i == page:
            page_list.append('<li class="active"><a href="/crm/depart/list/?page={}">{}</a></li>'.format(i, i))
        else:
            page_list.append('<li><a href="/crm/depart/list/?page={}">{}</a></li>'.format(i, i))

    if page == total_page_num:
        page_list.append('<li class="disabled"> <span aria-hidden="true">»</span>  </li>')
    else:
        page_list.append('<li><a href="/crm/depart/list/?page={}">»</a></li>'.format(page + 1))

    page_html = ''.join(page_list)

    all_depart = models.Department.objects.all()[(page - 1) * 10:page * 10]
    return render(request, 'depart_list.html',
                  {'all_depart': all_depart, 'page_html': page_html})


def depart_list(request):
    page = request.GET.get('page')
    query = request.GET.get('query', '')

    # title__contains=query
    # Q(title__contains=query)     Q(('title__contains',query))
    query_list = ['']

    count = models.Department.objects.filter(Q(('title__contains', query))).count()
    pager = Pagination(page, count, request.path_info)

    all_depart = models.Department.objects.filter(Q(('title__contains', query)))[pager.start:pager.end]
    return render(request, 'depart_list.html',
                  {'all_depart': all_depart, 'page_html': pager.page_html})


def depart_add(request):
    form_obj = DepartModelForm()
    if request.method == 'POST':
        form_obj = DepartModelForm(data=request.POST)
        if form_obj.is_valid():  # 对数据进行校验
            # 保存数据
            # models.Department.objects.create(**form_obj.cleaned_data)
            form_obj.save()
            return redirect(rev_url(request, 'depart_list'))
    return render(request, 'depart_form.html', {'form_obj': form_obj})


def depart_edit(request, edit_id):
    edit_obj = models.Department.objects.filter(id=edit_id).first()
    form_obj = DepartModelForm(instance=edit_obj)
    if request.method == 'POST':
        form_obj = DepartModelForm(data=request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(rev_url(request, 'depart_list'))
    return render(request, 'depart_form.html', {'form_obj': form_obj})


def depart_del(request, del_id):
    print(del_id)
    models.Department.objects.filter(id=del_id).delete()
    return redirect(reverse('depart_list'))
