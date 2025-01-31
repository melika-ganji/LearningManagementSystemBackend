from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from courses.models import Course, Category
from courses.serializers import CourseSerializer, CategorySerializer
from .serializers import UserSearchSerializer, CourseSearchSerializer, CategorySearchSerializer
from search.filters import UserFilter, CourseFilter, CategoryFilter


class UserSearchView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get(self, request, *args, **kwargs):
        user_role = request.user.role

        if user_role not in ["admin", "professor"]:
            return Response({"detail": "You are not authorized to search for users."},
                            status=status.HTTP_403_FORBIDDEN)

        query = request.query_params.get('query', None)

        if not query:
            return Response({"detail": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        if user_role == "admin":
            users = CustomUser.objects.filter(
                Q(phone_number__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(
                    last_name__icontains=query)
            )
        elif user_role == "professor":
            users = CustomUser.objects.filter(
                Q(role="student") &
                (Q(phone_number__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(
                    last_name__icontains=query))
            )
        else:
            users = CustomUser.objects.none()

        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseSearchView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)

        if not query:
            return Response({"detail": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        courses = Course.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategorySearchView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySearchSerializer
    permission_classes = [IsAuthenticated]  # Both students and professors
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)

        if not query:
            return Response({"detail": "Query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        categories = Category.objects.filter(Q(name__icontains=query))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
