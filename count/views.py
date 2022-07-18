from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from count import serializers
from count.models import Party, Member, Purchase

from count.utils import party_handle


class PurchaseAPIView(ListCreateAPIView):

    def get_queryset(self):
        return Purchase.objects.filter(party_id=self.kwargs.get('party_id'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PurchaseCreateSerializer
        return serializers.PurchaseSerializer


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = serializers.MembersSerializer


class ListOfPartiesViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.prefetch_related('member_set').all()
    serializer_class = serializers.DetailPartySerializer


class CountExpenses(APIView):

    def get(self, request, id):

        party = Party.objects.prefetch_related('member_set', 'purchase').get(id=id)

        response = []
        for member in party_handle(party):
            response.append(member.to_json())

        return Response(response)





