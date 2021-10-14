from django.db import models


class Register(models.Model):
    fio = models.CharField(verbose_name='ФИО', max_length=60)
    subject = models.CharField(verbose_name='Причина обращения ', max_length=90)
    r_date = models.DateField(verbose_name='Дата приема')
    time = models.CharField(verbose_name='Время приема', max_length=5)
    stol = models.IntegerField(verbose_name='Стол')


class Stol(models.Model):
    fio = models.CharField(verbose_name='ФИО', max_length=60)
    stol = models.IntegerField(verbose_name='Стол')

    def __str__(self):
        return '%s ' % self.fio


class Holiday(models.Model):
    stol = models.IntegerField(verbose_name='Стол')
    fio = models.ForeignKey(Stol, verbose_name='ФИО ', on_delete=models.CASCADE)
    date1 = models.DateField(verbose_name='Отпуск с')
    date2 = models.DateField(verbose_name='Отпуск до')
