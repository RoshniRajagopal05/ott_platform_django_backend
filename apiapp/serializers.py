from rest_framework import serializers
from .models import Movie
from .models import Watchlist
from .models import WatchHistory
from .models import User


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class WatchHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'movie', 'watched_at']