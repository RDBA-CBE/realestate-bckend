from rest_framework import serializers
from django.contrib.auth.models import Group
from ..models.address import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    group = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'group')

    def create(self, validated_data):
        group_name = validated_data.pop('group').capitalize()
        user = User.objects.create_user(**validated_data)
        if group_name in ['Buyer', 'Seller', 'Agent', 'Developer', 'Admin']:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        return user
