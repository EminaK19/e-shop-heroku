from rest_framework import serializers

from .models import Product, Category, Comment

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     price = serializers.DecimalField(max_digits=12, decimal_places=2)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    # read_only - отображается только при get запросе
    # write_only - отображается только при post запросе

    class Meta:
        model = Comment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def _get_image_url(self, obj):
        """method for get image url"""
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation
# можно сделать отдельно на лситинг отдельно на детали сериалайзеры чтобы добавить комментарии к деталям а не к листингу


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['description']

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        return representation


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'categories']
