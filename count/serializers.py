from rest_framework import serializers

from count.models import Party, Member, Purchase


class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = '__all__'


class MembersSerializer(serializers.ModelSerializer):
    expenses = ExpensesSerializer(source='member_purchase', many=True, read_only=True)

    class Meta:
        model = Member
        fields = '__all__'


class ListOfPartiesSerializer(serializers.ModelSerializer):
    members = MembersSerializer(source='member_party', many=True, read_only=True)

    class Meta:
        model = Party
        fields = ('id', 'date', 'description', 'members')


class DetailPartySerializer(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = ('date', 'description')