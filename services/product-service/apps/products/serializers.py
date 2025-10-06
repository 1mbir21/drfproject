from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "products_count", "slug", "description", "created_at"]

    def products_count(self, obj):
        return obj.product.filter(is_active=True).count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "category",
            "created_at",
            "category_name",
            "is_in_stock",
            "is_active",
            "stock_quantity",
            "image_url",
            "updated_at",
        ]


class ProductDetailSerializer(ProductSerializer):
    category = CategorySerializer(read_only=True)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "description",
            "category",
            "is_active",
            "stock_quantity",
            "image_url",
        ]
