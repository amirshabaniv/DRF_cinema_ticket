from rest_framework import serializers
from .models import Profile, User

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'age', 'bio', 'picture']