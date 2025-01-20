from django.urls import path
from accounts.views import (
    AdminProfileRetrieveUpdateDestroyView,
    ProfessorProfileRetrieveUpdateDestroyView,
    StudentProfileRetrieveUpdateDestroyView, RegisterView, LoginView
)

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('profile/admin/<int:pk>/', AdminProfileRetrieveUpdateDestroyView.as_view(), name='admin-profile-detail'),

    path('profile/professor/<int:pk>/', ProfessorProfileRetrieveUpdateDestroyView.as_view(),
         name='professor-profile-detail'),

    path('profile/student/<int:pk>/', StudentProfileRetrieveUpdateDestroyView.as_view(), name='student-profile-detail'),
]
