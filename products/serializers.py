from rest_framework import serializers
from .models import Product


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "target_amount",
            "funding_end_date",
            "one_time_funding_amount",
            "publisher",
        ]


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "funding_end_date",
            "one_time_funding_amount",
        ]


class FundingProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["one_time_funding_amount"]


class ProductSerializer(serializers.ModelSerializer):

    d_day = serializers.SerializerMethodField()
    achievment_rate = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "publisher_name",
            "description",
            "target_amount",
            "funding_end_date",
            "one_time_funding_amount",
            "d_day",
            "achievment_rate",
            "total_amount",
            "participants_count",
        ]

    def d_day(self, instance):
        return instance.d_day()

    def achievment_rate(self, instance):
        return instance.achievment_rate()

    def participants_count(self, instance):
        return instance.participants_count()
