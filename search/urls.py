from django.urls import path
from .views import UserSearchView, CourseSearchView, CategorySearchView

urlpatterns = [
    path('users/', UserSearchView.as_view(), name='search-users'),
    path('courses/', CourseSearchView.as_view(), name='search-courses'),
    path('categories/', CategorySearchView.as_view(), name='search-categories'),
]
