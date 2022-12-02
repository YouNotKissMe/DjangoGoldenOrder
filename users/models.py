from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, ValidationError, MinValueValidator

import datetime
from datetime import date as datenow


class Child(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True,
                                  validators=[MinValueValidator(
                                      limit_value=datenow((datetime.datetime.now().year - 14),
                                                          datetime.datetime.now().month,
                                                          datetime.datetime.now().day))])

    def clean(self):
        if datetime.datetime.now().year - self.birth_date.year >= 18:
            raise ValidationError(
                'Возраст ребенка не удовлетворяет требованиям')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Ребенок'
        verbose_name_plural = 'Дети'


class ProfileParents(models.Model):
    gender = [('Муж', 'Муж'), ('Жен', 'Жен')]
    key = models.OneToOneField(User, on_delete=models.CASCADE)
    gender_model = models.TextField(choices=gender, verbose_name='Пол', blank=True, null=True,
                                    default=gender[0][0])
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    childs = models.ManyToManyField(Child, on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True,
                                  validators=[MaxValueValidator(
                                      limit_value=datenow((datetime.datetime.now().year - 18),
                                                          datetime.datetime.now().month,
                                                          datetime.datetime.now().day))])

    def save(self, *args, **kwargs):
        # you can have regular model instance saves use this as well
        super(ProfileParents, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'

# Create your models here.
