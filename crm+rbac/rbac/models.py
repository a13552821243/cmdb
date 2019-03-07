from django.db import models


class Menu(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)
    weight = models.IntegerField(default=1)


class Permission(models.Model):
    url = models.CharField(verbose_name='含正则的URL地址', max_length=64)
    title = models.CharField(verbose_name='标题', max_length=32)
    name = models.CharField(verbose_name='URL别名', max_length=32)
    menu = models.ForeignKey('Menu', blank=True, null=True)
    parent = models.ForeignKey(to='self', blank=True, null=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色名')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色拥有的权限', blank=True)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField(to=Role, verbose_name='用户拥有的角色')

    class Meta:
        abstract = True  # 使用后数据库不生成表， 当做基类。
