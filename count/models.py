from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Sum
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from config.settings import USE_CACHE
from count.managers import CustomAccountManager


#TODO перенести его куда-то
def check_cache(key):
    def func_check_cache(func):
        def checking(self):
            if not USE_CACHE:
                data = func(self)
                return data
            else:
                cache_data = cache.get(str(self.id) + key)
                if cache_data is None:
                    data = func(self)
                    cache.set(str(self.id) + key, data, timeout=1)
                    return data
                else:
                    return cache_data
        return checking
    return func_check_cache


class PartyUser(AbstractBaseUser, PermissionsMixin):

    PAYMENT_CHOICES = [('SBER', 'Sberbank'),
                       ('TINKOFF', 'Tinkoff')]

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    phone_number = models.IntegerField("Номер телефона", blank=True, null=True)
    payment_method = models.CharField("Желаемый способ оплаты", choices=PAYMENT_CHOICES, default='SBER', max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name


class Party(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    date = models.DateField()
    description = models.CharField("Описание тусовки", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        if self.description is not None:
            return self.description
        else:
            return f"Мероприятие {str(self.date)}"

    @property
    def member_count(self) -> int:
        return self.member_set.all().count()

    @property
    @check_cache('budget')
    def budget(self) -> int:
        return self.purchase.all().aggregate(Sum('expenses')).get('expenses__sum')


class Member(models.Model):
    user = models.ForeignKey(PartyUser, on_delete=models.CASCADE, related_name='user_party', blank=True, null=True)
    name = models.CharField("Участник", max_length=100)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f"{self.name}"

    @property
    @check_cache('party_summary_purchases')
    def party_summary_purchases(self) -> float:
        res = self.member_purchase.all().aggregate(Sum('expenses')).get('expenses__sum')
        if res is None:
            return 0
        return res

    @check_cache('get_member_usage_purchase')
    def get_member_usage_purchase(self):
        purchases = self.party.purchase.exclude(id__in=list(self.member_exclude.all().values_list('purchase_id', flat=True)))
        return sum([purchase.avg_price_on_purchase() for purchase in purchases])


class Purchase(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='purchase')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_purchase')
    expenses = models.FloatField("Потратил", default=0)
    description = models.CharField("Описание траты", max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return f"{self.member} потратился на {self.description}"

    @check_cache('avg_price_on_purchase')
    def avg_price_on_purchase(self):
        return self.expenses/(self.party.member_count - self.purchase_exclude.all().count())


class PurchaseExclude(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_exclude')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_exclude')

    class Meta:
        verbose_name = 'Исключение'
        verbose_name_plural = 'Исключения'

    def __str__(self):
        return f"{self.member} не потратился на {self.purchase}"
