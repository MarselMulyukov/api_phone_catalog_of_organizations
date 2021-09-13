from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator 
from django.db import models

User = get_user_model()


class Company(models.Model):
    title = models.CharField(
        verbose_name='Название организации',
        max_length=50,
        unique=True
    )
    info = models.CharField(
        verbose_name='Описание организации',
        max_length=200
    )
    address = models.CharField(
        verbose_name='Адрес организации',
        max_length=100
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь внесший организацию в справочник',
        related_name='companies', on_delete=models.CASCADE)
    redactor = models.ManyToManyField(
        User,
        verbose_name='Пользователи с разрешением на редактирование',
        related_name='companies_to_edit')

    def __str__(self) -> str:
        return self.title


class Worker(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    name = models.CharField(verbose_name='ФИО работника', max_length=50)
    position = models.CharField(verbose_name='должность', max_length=50)
    private_phone = models.CharField(
        verbose_name='номер личного телефона',
        validators=[phoneNumberRegex,],
        max_length=16,
        blank=True,
        null=True
    )
    work_phone = models.CharField(
        verbose_name='номер рабочего телефона',
        validators=[phoneNumberRegex],
        max_length=16,
        blank=True
    )
    fax = models.CharField(
        verbose_name='номер факса',
        validators=[phoneNumberRegex],
        max_length=16,
        blank=True
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='workers'
    )

    def __str__(self) -> str:
        return self.name