from django.shortcuts import HttpResponse, render, redirect, reverse
from crm import models
from crm.forms.my_form import UserModelForm

def user_list(request):
    users = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {'users': users})


def user_add(request):
    form_obj = UserModelForm()
    if request.method == 'POST':
        form_obj = UserModelForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('user_list'))
    return render(request, 'change.html', {"form_obj": form_obj})
