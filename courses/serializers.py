from importlib.metadata import requires
from unicodedata import category

from rest_framework import serializers


from courses.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def validate(self, data):
        if self.instance is None:
            if 'name' not in data:
                raise serializers.ValidationError({'name': 'This field is required during creation.'})
        return data


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'price', 'changed_at']

    def validate(self, data):
        if self.instance is None:
            if 'price' not in data:
                raise serializers.ValidationError({'price': 'This field is required during creation.'})
        return data


class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = ['id', 'title', 'description']

    def validate(self, data):
        if self.instance is None:
            if 'title' not in data:
                raise serializers.ValidationError({'title': 'This field is required during creation.'})
        return data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text','course', 'created_at']

    def validate(self, data):
        if self.instance is None:
            if 'text' not in data:
                raise serializers.ValidationError({'text': 'This field is required during creation.'})
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)
    headings = HeadingSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'master','category', 'category_name', 'description', 'price', 'price_history',
            'headings', 'comments', 'startDate', 'studentsCount', 'created_at', 'updated_at',
        ]

    def validate(self, data):
        if self.instance is None:
            if 'name' not in data:
                raise serializers.ValidationError({'name': 'This field is required during creation.'})
            if 'category' not in data:
                raise serializers.ValidationError({'category': 'This field is required during creation.'})
            if 'price' not in data:
                raise serializers.ValidationError({'price': 'This field is required during creation.'})
        return data


class CourseContentSerializer(serializers.ModelSerializer):
    # course = CourseSerializer(read_only=True)
    course_name = serializers.ReadOnlyField(source='course.name')

    class Meta:
        model = CourseContent
        fields = ['id', 'course', 'course_name', 'content_type', 'title', 'contentFile', 'textContent', 'created_at']

    def validate(self, data):
        if self.instance is None:
            if 'course' not in data:
                raise serializers.ValidationError({'course': 'This field is required during creation.'})
            if 'content_type' not in data:
                raise serializers.ValidationError({'content_type': 'This field is required during creation.'})
            if 'title' not in data:
                raise serializers.ValidationError({'title': 'This field is required during creation.'})
        return data


class PurchaseSerializer(serializers.ModelSerializer):
    from accounts.serializers import CustomUserSerializer

    student = CustomUserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'student', 'course', 'amount_paid', 'purchase_date']

    def validate(self, data):
        if self.instance is None:
            if 'course' not in data:
                raise serializers.ValidationError({'course': 'This field is required during creation.'})
            if 'student' not in data:
                raise serializers.ValidationError({'student': 'This field is required during creation.'})
            if 'amount_paid' not in data:
                raise serializers.ValidationError({'amount_paid': 'This field is required during creation.'})
            if 'purchase_date' not in data:
                raise serializers.ValidationError({'purchase_date': 'This field is required during creation.'})
        return data
