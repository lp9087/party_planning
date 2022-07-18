from rest_framework import serializers

from count.models import Party, Member, Purchase


class MembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'name')


class PurchaseCreateSerializer(serializers.ModelSerializer):
    member = serializers.RelatedField(
        source='member_purchase',
        read_only=True,
    )

    class Meta:
        model = Purchase
        fields = ('expenses', 'description', 'member')


class PurchaseSerializer(serializers.ModelSerializer):
    member = serializers.RelatedField(
        source='member_purchase',
        read_only=True,
    )

    class Meta:
        model = Purchase
        fields = ('id', 'member', 'expenses', 'description')


class ListOfPartiesSerializer(serializers.ModelSerializer):
    members = MembersSerializer(source='member_set', many=True, read_only=True)

    class Meta:
        model = Party
        fields = ('id', 'date', 'description', 'members')


class DetailPartySerializer(serializers.ModelSerializer):
    members = MembersSerializer(source='member_set', many=True, read_only=True)

    class Meta:
        model = Party
        fields = ('date', 'description', 'members', 'budget', 'member_count')
