from rest_framework import serializers
from catalog.models import Author, Book, BookImage

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = ['url']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)
    images = serializers.SerializerMethodField(read_only=True)

    def get_images(self, obj):
        images = BookImage.objects.filter(book_id=obj.id)
        serializer = BookImageSerializer(instance=images, many=True)
        return serializer.data

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(**author_data)
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(**author_data)
        instance.author = author
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
