from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views


urlpatterns = format_suffix_patterns ([
    path('movie/', views.MovieViewSet.as_view({'get':'list'})),
    path('movie/<int:pk>/', views.MovieViewSet.as_view({'get':'retrieve'})),
    path('review/', views.ReviewCreateViewSet.as_view({'post':'create'})),
    path('rating/', views.AddStarRatingViewSet.as_view({'post':'create'})),
    path('actors/', views.ActorsViewSet.as_view({'get':'list'})),
    path('actors/<int:pk>/', views.ActorsViewSet.as_view({'get':'retrieve'}))
])