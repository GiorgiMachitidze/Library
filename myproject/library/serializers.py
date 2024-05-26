from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'born_date']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Book
        fields = '__all__'


class ReservationSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class PopularBookSerializer(serializers.ModelSerializer):
    all_reserved_quantity = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'all_reserved_quantity']


class BookIssueCountSerializer(serializers.ModelSerializer):
    issue_count = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'issue_count']


class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = '__all__'


class TopLateReturnedBooksSerializer(serializers.ModelSerializer):
    late_return_count = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['title', 'late_return_count']


class TopLateReturnedUserSerilizer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    late_return_count = serializers.IntegerField()

    class Meta:
        model = Client
        fields = ['user', 'late_return_count']
