from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from accounts.serializers import *


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        if request.user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_data = {'phone_number': request.data.get('phone_number'), 'password': request.data.get('password'),
                     'role': request.data.get('role'),
                     }

        user_serializer = CustomUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        role = request.data.get('role')

        if role == 'admin':
            profile_data = {'user': user.id, 'name': request.data.get('name', ),
                            'lastName': request.data.get('lastName'), 'username': request.data.get('username')}
            profile_serializer = AdminProfileSerializer(data=profile_data)

        elif role == 'professor':
            profile_data = {'user': user.id, 'name': request.data.get('name', ),
                            'lastName': request.data.get('lastName'), 'specialty': request.data.get('specialty'),
                            'workbook': request.data.get('workbook'), 'image': request.data.get('image'),
                            'description': request.data.get('description')}
            profile_serializer = ProfessorProfileSerializer(data=profile_data)

        elif role == 'student':
            profile_data = {'user': user.id, 'name': request.data.get('name', ),
                            'lastName': request.data.get('lastName'), 'username': request.data.get('username'),
                            'national_code': request.data.get('national_code')}
            profile_serializer = StudentProfileSerializer(data=profile_data)
        else:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save(user=user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': user_serializer.data,
            'profile': profile_serializer.data,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens_and_user = serializer.save()
        return Response(tokens_and_user, status=status.HTTP_200_OK)


class AdminProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return AdminProfile.objects.get(pk=self.kwargs['pk'])
        except AdminProfile.DoesNotExist:
            raise NotFound("Admin profile not found.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Allow partial updates
        instance = self.get_object()  # Get the existing profile instance

        # Extract and handle the 'user' data if provided
        user_data = request.data.pop('user', None)
        if user_data:
            user_serializer = CustomUserSerializer(instance=instance.user, data=user_data, partial=partial)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Update the profile instance with the remaining data
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.is_active = False
        instance.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfessorProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return ProfessorProfile.objects.get(pk=self.kwargs['pk'])
        except ProfessorProfile.DoesNotExist:
            raise NotFound("Professor profile not found.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_data = request.data.pop('user', None)

        if user_data:
            user_serializer = CustomUserSerializer(instance=instance.user, data=user_data, partial=partial)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.is_active = False
        instance.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return StudentProfile.objects.get(pk=self.kwargs['pk'])
        except StudentProfile.DoesNotExist:
            raise NotFound("Student profile not found.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_data = request.data.pop('user', None)

        if user_data:
            user_serializer = CustomUserSerializer(instance=instance.user, data=user_data, partial=partial)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user.is_active = False
        instance.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
