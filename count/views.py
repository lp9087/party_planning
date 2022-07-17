from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from count import serializers
from count.models import Party, Member, Purchase
from django.db.models import Sum

from count.utils import party_handle


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = serializers.ExpensesSerializer


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = serializers.MembersSerializer


class ListOfPartiesViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()

    serializer_classes = {
        'list': serializers.ListOfPartiesSerializer,
        'retrieve': serializers.DetailPartySerializer,
    }
    default_serializer_class = serializers.ListOfPartiesSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class CountExpenses(APIView):

    def get(self, request, id):

        party = Party.objects.prefetch_related('dateparty', 'date_exp').get(id=id)

        response = []
        for member in party_handle(party):
            response.append(member.to_json())

        return Response(response)





