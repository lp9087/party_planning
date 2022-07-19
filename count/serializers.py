from rest_framework import serializers

from count.models import Party, Member, Purchase


class MembersCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Member.objects.create(party_id=self.context.get('view').kwargs.get('party_id'), **validated_data)

    class Meta:
        model = Member
        fields = ('user', 'name',)


class MembersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'name')


class PurchaseCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Purchase.objects.create(party_id=self.context.get('view').kwargs.get('party_id'), **validated_data)

    class Meta:
        model = Purchase
        fields = ('member', 'expenses', 'description')


class PurchaseSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()

    class Meta:
        model = Purchase
        fields = ('id', 'member', 'expenses', 'description')


class ListOfPartiesSerializer(serializers.ModelSerializer):
    members = MembersListSerializer(source='member_set', many=True, read_only=True)

    class Meta:
        model = Party
        fields = ('id', 'date', 'description', 'members')


class DetailPartySerializer(serializers.ModelSerializer):
    members = MembersListSerializer(source='member_set', many=True, read_only=True)

    class Meta:
        model = Party
        fields = ('id', 'date', 'description', 'members', 'budget', 'member_count')
