from rest_framework import serializers
from .models import (Movie, 
                    Review, 
                    Rating, 
                    Actor)

#Фильтр комментов, родительский
class FilterReviewListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

#Вывод рекурсивно, дочерний
class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data 

#Список актеров и режиссеров
class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')

#Описание актера или/и режиссера
class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

#Список фильмов
class MovieListSerializer(serializers.ModelSerializer):

    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')

#Добавление Отзыва
class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

#Вызод отзыва
class ReviewSerializer(serializers.ModelSerializer):

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')

#Полный фильм
class MovieDetailSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorDetailSerializer(read_only=True, many=True)
    actors = ActorDetailSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)


    class Meta:
        model = Movie
        exclude = ('draft',)

#Добавление Рейтинга Пользователя
class CreateRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip = validated_data.get('ip', None),
            movie = validated_data.get('movie', None),
            defaults = {'star': validated_data.get('star')})
        return rating