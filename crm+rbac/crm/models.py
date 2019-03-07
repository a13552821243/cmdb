from django.db import models
from rbac.models import UserInfo as RbacUserInfo


# Create your models here.
class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(max_length=32, verbose_name='部门名称')

    # class Meta:
    #     db_table='xxxx'
    def __str__(self):
        return self.title


class UserInfo(RbacUserInfo):
    # name = models.CharField(max_length=32, verbose_name='用户名')
    # password = models.CharField(max_length=32, verbose_name='密码')
    gener_choice = ((0, '男'), (1, '女'))
    gener = models.IntegerField(choices=gener_choice)
    depart = models.ForeignKey(to='Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    课程表
    如：
        Linux基础
        Linux架构师
        Python自动化
        Python全栈
    """
    name = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.name


class School(models.Model):
    """
    校区表
    如：
        北京昌平校区
        上海浦东校区
        深圳南山校区
    """
    title = models.CharField(verbose_name='校区名称', max_length=32)

    def __str__(self):
        return self.title


class ClassList(models.Model):
    """
    班级表
    如：
        Python全栈  面授班  5期  10000  2017-11-11  2018-5-11
    """
    school = models.ForeignKey(verbose_name='校区', to='School')
    course = models.ForeignKey(verbose_name='课程名称', to='Course')
    semester = models.IntegerField(verbose_name="班级(期)")  # 11
    price = models.IntegerField(verbose_name="学费")
    start_date = models.DateField(verbose_name="开班日期")
    graduate_date = models.DateField(verbose_name="结业日期", null=True, blank=True)

    # related_name用于orm的反向查找，替代 classlist_set
    tutor = models.ForeignKey(verbose_name='班主任', to='UserInfo', related_name='classes')
    teachers = models.ManyToManyField(verbose_name='任课老师', to='UserInfo', related_name='teach_classes')

    memo = models.CharField(verbose_name='说明', max_length=255, blank=True, null=True)

    def __str__(self):
        return "{0}({1}期)".format(self.course.name, self.semester)

    def name(self):
        return "{}-{}({})".format(self.school.title, self.course.name, self.semester)

    def show_teachers(self):
        return '|'.join([i.name for i in self.teachers.all()])
