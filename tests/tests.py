import datetime

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from count.models import Party, Member, Purchase, PurchaseExclude


class CountPartyTestCase(TestCase):
    def setUp(self):
        party = Party.objects.create(date=datetime.date.today(), description="party")

        kirill = Member.objects.create(name="kirill", party=party)
        Member.objects.create(name="alex", party=party)
        yarik = Member.objects.create(name="yarik", party=party)
        renat = Member.objects.create(name="renat", party=party)
        alina = Member.objects.create(name="alina", party=party)

        Purchase.objects.create(party=party, member=yarik, expenses=2200, description="alchohol")
        Purchase.objects.create(party=party, member=renat, expenses=2200, description="food")
        exclude_purchase = Purchase.objects.create(party=party, member=alina, expenses=1200, description="hookah")

        PurchaseExclude.objects.create(purchase=exclude_purchase, member=kirill)

    def test_count_party(self):
        client = APIClient()
        party = Party.objects.all().first()
        responce = client.get(reverse('count_exp', args=[party.id]))
        expected_json = [
            {
                "sender": "kirill",
                "receiver": "yarik",
                "money": 880
            },
            {
                "sender": "alex",
                "receiver": "yarik",
                "money": 140
            },
            {
                "sender": "alex",
                "receiver": "renat",
                "money": 1020
            },
            {
                "sender": "alex",
                "receiver": "alina",
                "money": 20
            }
        ]
        self.assertEqual(responce.data, expected_json)
