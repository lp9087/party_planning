from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from count import serializers
from count.models import Party, Member, Purchase

from count.utils import party_handle


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    #serializer_class = serializers.PurchaseSerializer
    lookup_url_kwarg = "party_id"

    serializer_classes = {
        'create': serializers.PurchaseCreateSerializer,
        'list': serializers.PurchaseSerializer,
    }
    default_serializer_class = serializers.PurchaseSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class MembersViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = serializers.MembersSerializer


class ListOfPartiesViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.prefetch_related('member_set').all()
    serializer_class = serializers.DetailPartySerializer


class CountExpenses(APIView):

    def get(self, request, id):

        party = Party.objects.prefetch_related('members', 'purchase').get(id=id)

        response = []
        for member in party_handle(party):
            response.append(member.to_json())

        return Response(response)





