from rest_framework import serializers

from accounts.serializers import CustomUserSerializer
from courses.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'price', 'changed_at']


class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = ['id', 'title', 'description']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)
    headings = HeadingSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    categoryName = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'master', 'category', 'category_name', 'description', 'price', 'price_history',
            'headings', 'comments', 'start_date', 'students_count', 'created_at', 'updated_at',
        ]

class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = ['id', 'course', 'content_type', 'title', 'content_file', 'text_content', 'created_at']


class PurchaseSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(read_only=True)  # Serialize student details
    course = CourseSerializer(read_only=True)  # Serialize course details

    class Meta:
        model = Purchase
        fields = ['id', 'student', 'course', 'amount_paid', 'purchase_date']
        read_only_fields = ['id', 'student', 'course', 'amount_paid', 'purchase_date']