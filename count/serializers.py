from rest_framework import serializers

from count.models import Party, Member, Purchase


class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = '__all__'


class MembersSerializer(serializers.ModelSerializer):
    expenses = ExpensesSerializer(source='member_exp', many=True, read_only=True)

    class Meta:
        model = Member
        fields = '__all__'


class ListOfPartiesSerializer(serializers.ModelSerializer):
    members = MembersSerializer(source='dateparty', many=True, read_only=True)

    class Meta:
        model = Party
        fields = ('id', 'date', 'description', 'members')


class DetailPartySerializer(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = ('date', 'description')