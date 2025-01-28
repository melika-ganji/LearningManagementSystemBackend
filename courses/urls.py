from django.urls import path
from courses.views import (
    CategoryListCreateView,
    CourseListCreateView,
    CourseRetrieveUpdateDestroyView,
    HeadingListCreateView,
    CommentListCreateView,
    CourseContentListCreateView,
    CourseContentRetrieveUpdateDestroyView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),
    path('headings/', HeadingListCreateView.as_view(), name='heading-list-create'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('contents/', CourseContentListCreateView.as_view(), name='content-list-create'),
    path('contents/<int:pk>/', CourseContentRetrieveUpdateDestroyView.as_view(), name='content-detail'),
]