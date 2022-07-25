from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins

from count import serializers
from count.models import Party, Member, Purchase, PurchaseExclude
from count.utils.utils import party_handle


class PurchaseAPIView(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):

    def get_queryset(self):
        return Purchase.objects.select_related('member').filter(party_id=self.kwargs.get('party_id'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PurchaseCreateSerializer
        return serializers.PurchaseSerializer


class MembersAPIView(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):

    def get_queryset(self):
        return Member.objects.filter(party_id=self.kwargs.get('party_id'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.MembersCreateSerializer
        return serializers.MembersListSerializer


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


class PurchaseExcludeAPIView(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = PurchaseExclude.objects.select_related('purchase', 'member').all()
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['member', 'purchase']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PurchaseExcludeCreateSerializer
        return serializers.PurchaseExcludeSerializer





