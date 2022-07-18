from rest_framework import serializers

from count.models import Party, Member, Purchase


class PurchaseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('member', 'expenses', 'description')


class PurchaseSerializer(serializers.ModelSerializer):

    member = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Purchase
        fields = ('id', 'member', 'expenses', 'description')


class MembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'name')


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
