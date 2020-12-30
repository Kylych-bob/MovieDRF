from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .service import get_client_ip
from .models import Movie, Actor
from django.db import models
from .serializers import (MovieListSerializer, 
                         MovieDetailSerializer, 
                         ReviewCreateSerializer,
                         CreateRatingSerializer,
                         ActorDetailSerializer,
                         ActorListSerializer)


#Вывод список фильмов
class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter = models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
            # rating_user=models.Case(
            #     models.When(ratings__ip=get_client_ip(request), then=True),
            #         default=False,
            #         output_field=models.BooleanField()
            #     ),
        # )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

#Вывод фильма
class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)

#Добавление отзыва к фильму
class ReviewCreateView(APIView):
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)

#Добавление рейтинга к фильму
class AddStarRatingView(APIView):

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)

#Список Актеров
class ActorsListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

#Вывод Актера или/и Режиссера
class ActorsDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer

# from django.shortcuts import render, redirect
# from django.db.models import Q
# from django.http import JsonResponse, HttpResponse
# # Create your views here.
# from django.views.generic.base import View 
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from .models import Movie, Category, Actor, Genre, Rating
# from .forms import ReviewForm, RatingForm


# '''Жанры и года выхода фильмов'''
# class GenreYear:
#         def get_genres(self):
#                 return Genre.objects.all()
#         def get_years(self):
#                 return Movie.objects.filter(draft=False).values('year')

# '''Список фильмов'''
# class MoviesView(ListView, GenreYear):
#         model = Movie
#         queryset = Movie.objects.filter(draft=False)
#         paginate_by = 2

# '''Полное описание фильма'''
# class MovieDetailView(DetailView, GenreYear):
#         model = Movie
#         queryset = Movie.objects.filter(draft=False)
#         slug_field = 'url'

#         def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 context['star_form'] = RatingForm()
#                 context['form'] = ReviewForm()
#                 return context

# '''Отзывы'''
# class AddReview(View):
#         def post(self, request, pk):
#                 form = ReviewForm(request.POST)
#                 movie = Movie.objects.get(id=pk)
#                 if form.is_valid():
#                         form = form.save(commit=False)
#                         if request.POST.get('parent', None):
#                                 form.parent_id = int(request.POST.get('parent'))
#                         form.movie = movie 
#                         form.save()
#                 return redirect(movie.get_absolute_url()) 

# '''Вывод информации о актере'''
# class ActorView(DetailView, GenreYear):
#         model = Actor
#         template_name = 'movies/actor.html'
#         slug_field = 'name'

# '''Фильтр фильмов'''
# class FilterMoviesView(ListView, GenreYear):
#     paginate_by = 5

#     def get_queryset(self):
#         queryset = Movie.objects.filter(
#             Q(year__in=self.request.GET.getlist('year')) |
#             Q(genres__in=self.request.GET.getlist('genre'))
#         ).distinct()
#         return queryset

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
#         context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
#         return context

# '''Фильтр фильмов в json'''
# class JsonFilterMoviesView(ListView):
#         def get_queryset(self):
#                 queryset = Movie.objects.filter(
#                         Q(year__in = self.request.GET.getlist('year')) |
#                         Q(genres__in = self.request.GET.getlist('genre'))
#                 ).distinct().values('title', 'tagline', 'url', 'poster')
#                 return queryset
#         def get(self, request, *args, **kwargs):
#                 queryset = list(self.get_queryset())
#                 return JsonResponse ({'movies': queryset}, safe=False)


# '''Добавление рейтинга фильму'''
# class AddStarRating(View):
   
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip

#     def post(self, request):
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             Rating.objects.update_or_create(
#                 ip=self.get_client_ip(request),
#                 movie_id=int(request.POST.get('movie')),
#                 defaults={'star_id': int(request.POST.get('star'))}
#             )
#             return HttpResponse(status=201)
#         else:
#             return HttpResponse(status=400)

# '''Поиск'''
# class Search(ListView, GenreYear):
#         paginate_by = 3

#         def get_queryset(self):
#                 return Movie.objects.filter(title__icontains=self.request.GET.get('q'))
#         def get_context_data(self, *args, **kwargs):
#                 context = super().get_context_data(*args, **kwargs)
#                 context['q'] = f'q = {self.request.GET.get("q")}&'
#                 return context