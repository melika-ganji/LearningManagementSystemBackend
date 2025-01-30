from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser, AdminProfile, ProfessorProfile, StudentProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True},
            'role': {'required': True}
        }

    def create(self, validated_data):
        if validated_data['role'] == 'admin':
            return CustomUser.objects.create_superuser(**validated_data)
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class AdminProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    lastName = serializers.CharField(required=False)

    class Meta:
        model = AdminProfile
        fields = ['user', 'name', 'lastName', 'username']

    def validate(self, data):
        if self.instance is None:
            if 'user' not in data:
                raise serializers.ValidationError({'user': 'This field is required during creation.'})
            if 'name' not in data:
                raise serializers.ValidationError({'name': 'This field is required during creation.'})
            if 'lastName' not in data:
                raise serializers.ValidationError({'lastName': 'This field is required during creation.'})
            if 'username' not in data:
                raise serializers.ValidationError({'username': 'This field is required during creation.'})
        return data


class ProfessorProfileSerializer(serializers.ModelSerializer):
    from courses.serializers import CourseSerializer
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    specialty = serializers.CharField(required=False)
    workbook = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)
    created_courses = CourseSerializer(source='user.course_set', many=True)

    class Meta:
        model = ProfessorProfile
        fields = ['user','name', 'lastName', 'specialty', 'workbook', 'image', 'description', 'created_courses']

    def validate(self, data):
        if self.instance is None:
            if 'user' not in data:
                raise serializers.ValidationError({'user': 'This field is required during creation.'})
            if 'name' not in data:
                raise serializers.ValidationError({'name': 'This field is required during creation.'})
            if 'lastName' not in data:
                raise serializers.ValidationError({'lastName': 'This field is required during creation.'})
            if 'speciality' not in data:
                raise serializers.ValidationError({'speciality': 'This field is required during creation.'})
            if 'workbook' not in data:
                raise serializers.ValidationError({'lastName': 'This field is required during creation.'})
        return data

    def create(self, validated_data):
        return ProfessorProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StudentProfileSerializer(serializers.ModelSerializer):
    from courses.serializers import CourseSerializer
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    username = serializers.CharField(required=False)
    national_code = serializers.CharField(required=False)
    purchased_courses = CourseSerializer(many=True)

    class Meta:
        model = StudentProfile
        fields = ['user', 'name', 'lastName', 'username', 'national_code', 'purchased_courses']

    def validate(self, data):
        if self.instance is None:
            if 'user' not in data:
                raise serializers.ValidationError({'user': 'This field is required during creation.'})
            if 'name' not in data:
                raise serializers.ValidationError({'name': 'This field is required during creation.'})
            if 'lastName' not in data:
                raise serializers.ValidationError({'lastName': 'This field is required during creation.'})
            if 'username' not in data:
                raise serializers.ValidationError({'username': 'This field is required during creation.'})
            if 'national_code' not in data:
                raise serializers.ValidationError({'national_code': 'This field is required during creation.'})
        return data

    def create(self, validated_data):
        return StudentProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data['phone_number']
        password = data['password']

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'phone_number': user.phone_number,
                'role': user.role,
            },
        }
