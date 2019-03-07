from django import forms
from crm import models
from django.core.validators import ValidationError


class DepartModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "部门名称"})
        }
        error_messages = {
            'title': {
                'required': '不能为空'
            }
        }


class UserModelForm(forms.ModelForm):
    re_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.UserInfo
        fields = [ 're_password', 'gener', 'depart']
        exclude = []

        labels = {
            'name': '用户名',
            'password': '密码',
            'gener': '性别',
            'depart': '部门',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'gener': forms.Select(attrs={'class': 'form-control'}),
            'depart': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'name': {'required': '不能为空'}
        }

    def clean_re_password(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return re_pwd
        raise ValidationError('两次密码不一致')

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # self.fields['semester'].widget.


class ClassesModelForm(BootstrapModelForm):
    class Meta:
        model = models.ClassList
        fields = "__all__"
