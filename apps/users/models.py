from django.db import models
from django.contrib.auth.models import AbstractUser

from storage import ImgStorage


class User(AbstractUser):
    username = models.CharField(max_length=11, unique=True, verbose_name="联系方式")
    avatar = models.ImageField(upload_to='avatar/%Y/%m', storage=ImgStorage(), blank=True, verbose_name="头像")
    truename = models.CharField(max_length=10, blank=True, verbose_name="真实姓名")
    usertype = models.IntegerField(choices=((1, '司机'), (2, '非司机')), default=2, verbose_name="用户类型")

    can_apply = models.BooleanField(default=True, verbose_name="能否预约")

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.usertype == 1:
            self.can_apply = False

        super(User, self).save()

    def get_now_reserve(self):
        return self.ucenterreservewrapper_set.all().filter(reserve_status=False)

    def get_done_reserve(self):
        return self.ucenterreservewrapper_set.all().filter(reserve_status=True)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Driver(models.Model):
    user = models.OneToOneField(User, verbose_name="关联的用户")
    number = models.CharField(max_length=10, blank=True, verbose_name="车牌号")
    type = models.IntegerField(choices=((1, "小车司机"), (2, "校车司机"), (3, "管理者")), verbose_name="司机类型")
    status = models.IntegerField(choices=((0, "非空闲"), (1, "空闲")), default=0, verbose_name="状态")

    class Meta:
        verbose_name = "司机"
        verbose_name_plural = verbose_name


class UcenterReserveWrapper(models.Model):
    user = models.ForeignKey(User)
    reserve_pk = models.IntegerField()
    reserve_type = models.IntegerField(choices=((1, '校车'), (2, "专车")))
    reserve_status = models.BooleanField(default=False)

    def __str__(self):
        return self.get_reserve_type_display()
