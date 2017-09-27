from django.db import models
from django.utils import timezone

from users.models import User, Driver


class SchoolBusTimeSchedules(models.Model):
    '''
    出行时刻
    '''
    date_schedule = models.CharField(max_length=10, verbose_name="时刻")

    def __str__(self):
        return self.date_schedule

    class Meta:
        verbose_name = "发车时间"
        verbose_name_plural = verbose_name


class SchoolBusWeekSchedules(models.Model):
    '''
    校车一周中每天的出行时刻
    '''
    week = models.IntegerField(
        choices=((1, "星期一"), (2, "星期二"), (3, "星期三"), (4, "星期四"), (5, "星期五"), (6, "星期六"), (7, "星期天")), verbose_name="星期")
    time = models.ManyToManyField(SchoolBusTimeSchedules, verbose_name="发车时间")

    def __str__(self):
        return self.get_week_display()

    class Meta:
        verbose_name = "一周发车时刻"
        verbose_name_plural = verbose_name


class SchoolBus(models.Model):
    '''
    校车类
    通过定时任务会在每天凌晨依据SchoolBusWeekSchedules来创建这天的所有SchoolBus对象
    一个SchoolBus代表一个班次，其存放了本班次的所有信息
    '''
    schedule = models.ForeignKey(SchoolBusTimeSchedules, verbose_name="时刻")
    num_reserve = models.IntegerField(default=0, verbose_name="预约人数")
    num_seats = models.IntegerField(blank=True, null=True, default=47, verbose_name="总座位数")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.schedule.date_schedule

    class Meta:
        verbose_name = "校车班次"
        verbose_name_plural = verbose_name
        ordering = ['-date']


class SchoolBusReserve(models.Model):
    '''
    校车预约类
    当用户发起乘坐校车申请时会创建
    '''
    user = models.ForeignKey(User, verbose_name="用户")
    schoolbus = models.ForeignKey(SchoolBus, verbose_name="校车班次")
    date_reserve = models.DateTimeField(default=timezone.now, verbose_name="发起预约时间")
    is_done = models.BooleanField(default=False, verbose_name="是否完成")

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.is_done:
            self.schoolbus.num_reserve = self.schoolbus.num_reserve + 1
        self.schoolbus.save()
        super(SchoolBusReserve, self).save()

    class Meta:
        verbose_name = "校车预约"
        verbose_name_plural = verbose_name


class SpecialCar(models.Model):
    '''
    专车类
    用于完成专车匹配/预约相关功能
    '''
    driver = models.OneToOneField(Driver, verbose_name="专车司机")
    num_user = models.IntegerField(default=0, verbose_name="搭乘人数")
    status = models.BooleanField(default=False, verbose_name="状态", help_text="False不能匹配，True可匹配")
    users = models.ManyToManyField(User, blank=True, verbose_name="乘坐用户")

    def __str__(self):
        return self.driver.user.username

    def  get_all_users_in_car(self):
        return self.users.all().order_by('-specialcartravel')

    class Meta:
        verbose_name = "专车"
        verbose_name_plural = verbose_name


class SpecialCarTravel(models.Model):
    '''
    专车匹配类
    当用户发起一个专车出行匹配（匹配到车辆）会被创建
    '''
    PLACE_CHOICE = ((1, "大花岭"), (2, "街道口"), (3, "光谷"), (4, "武昌站"), (5, "汉口火车站"), (6, "武汉站"))

    user = models.ForeignKey(User, verbose_name="用户")
    car = models.ForeignKey(SpecialCar, verbose_name="专车")
    place = models.IntegerField(choices=PLACE_CHOICE,verbose_name="目的地")

    is_accept = models.BooleanField(default=False, verbose_name="是否接受")
    is_done = models.BooleanField(default=False, verbose_name="是否完成")
    date_travel = models.DateTimeField(default=timezone.now, verbose_name="出行时间")

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_all_place():
        place_list = []
        for i in SpecialCarTravel.PLACE_CHOICE:
            place_list.append(i[1])
        return place_list


    class Meta:
        verbose_name = "专车出行申请"
        verbose_name_plural = verbose_name
        ordering = ['-date_travel']


class Chartered(models.Model):
    phone = models.CharField(max_length=11, verbose_name="包车联系方式")

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "包车"
        verbose_name_plural = verbose_name
