from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from crm.forms.my_form import ClassesModelForm
from django.db.models import Q
from crm.utils.pager import Pagination


def class_list(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page', '')

    # title__contains=query
    # Q(title__contains=query)     Q(('title__contains',query))
    query_list = ['semester', 'start_date']
    q = Q()
    q.connector = 'OR'
    for i in query_list:
        q.children.append(Q(('{}__contains'.format(i), query)))

    all_classes = models.ClassList.objects.filter(q)
    pager = Pagination(page, all_classes.count(), request.path_info,request.GET, 2)

    return render(request, 'classes_list.html',
                  {"all_classes": all_classes[pager.start:pager.end],
                   'page_html': pager.page_html
                   })


def class_add(request):
    form_obj = ClassesModelForm()
    if request.method == 'POST':
        form_obj = ClassesModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('class_list'))
    return render(request, 'change.html', {'form_obj': form_obj})


def class_edit(request, edit_id):
    obj = models.ClassList.objects.filter(pk=edit_id).first()
    form_obj = ClassesModelForm(instance=obj)
    if request.method == 'POST':
        form_obj = ClassesModelForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('class_list'))
    return render(request, 'change.html', {'form_obj': form_obj})


def classes(request, edit_id=None):
    obj = models.ClassList.objects.filter(pk=edit_id).first()
    form_obj = ClassesModelForm(instance=obj)
    if request.method == 'POST':
        form_obj = ClassesModelForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('class_list'))
    return render(request, 'change.html', {'form_obj': form_obj})
