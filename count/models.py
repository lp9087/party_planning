from django.db import models
from django.db.models import Sum


class Party(models.Model):
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
        return self.dateparty.all().count()


class Member(models.Model):
    name = models.CharField("Участник", max_length=100)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='dateparty')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f"{self.party} {self.name}"

    @property
    def party_summary_purchases(self) -> float:
        res = self.member_exp.all().aggregate(Sum('expenses')).get('expenses__sum')
        if res is None:
            return 0
        return res

    def get_member_usage_purchase(self):
        purchases = self.party.date_exp.exclude(id__in=list(self.membering.all().values_list('purchase_id', flat=True)))
        return sum([purchase.avg_price_on_purchase() for purchase in purchases])


class Purchase(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='date_exp')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_exp')
    expenses = models.DecimalField("Потратил", decimal_places=2, max_digits=10, default=0)
    description = models.CharField("Описание траты", max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return f"{self.member} потратился на {self.description}"

    def avg_price_on_purchase(self):
        return self.expenses/(self.party.member_count - self.purchasing.all().count())


class PurchaseExclude(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchasing')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='membering')

    class Meta:
        verbose_name = 'Исключение'
        verbose_name_plural = 'Исключения'

    def __str__(self):
        return f"{self.member} не потратился на {self.purchase}"
