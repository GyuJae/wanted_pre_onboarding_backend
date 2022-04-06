from rest_framework import serializers

from products.models import Product
from .models import User


class UserSerializer(serializers.ModelSerializer):

    products = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all()
    )

    class Meta:
        model = User
        fields = "__all__"
        read_only_field = ["products"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
