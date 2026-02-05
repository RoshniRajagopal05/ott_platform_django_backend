from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from apiapp.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK,  HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,HTTP_201_CREATED
from rest_framework.authtoken.models import Token
from .serializers import  MovieSerializer,WatchlistSerializer,WatchHistorySerializer
from .models import Movie,Watchlist,WatchHistory



@api_view(['POST'])
@permission_classes((AllowAny,))
def Signup(request):
    email  = request.data.get("email")
    password = request.data.get("password")
    name = request.data.get("name")

    if not name or not email or not password:
        return Response({'message': 'All fields are required'}, status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'message': 'Email already exists'}, status=HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(email=email, password=password)
    user.name = name
    user.save()

    return Response({'message': 'User created successfully. Please log in.'}, status=HTTP_200_OK)




@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({'error': 'Please provide both email and password'}, status=HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist. Please sign up.'}, status=HTTP_404_NOT_FOUND)

    if not check_password(password, user.password):
        return Response({'error': 'Invalid password'}, status=HTTP_404_NOT_FOUND)

   
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
    }, status=HTTP_200_OK)



@api_view(["GET" ])
@permission_classes([IsAuthenticated])
def movie_list(request):

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)




@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def watchlist_view(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = WatchlistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        watchlist = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        watchlist_id = request.data.get('id')
        if not watchlist_id:
            return Response({'error': 'Watchlist ID is required'}, status=HTTP_400_BAD_REQUEST)
        try:
            watchlist_item = Watchlist.objects.get(id=watchlist_id, user=request.user)
            watchlist_item.delete()
            return Response({'message': 'Removed from watchlist'}, status=HTTP_204_NO_CONTENT)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Watchlist item not found'}, status=HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watch_history_view(request):
    if request.method == 'POST':
        movie_id = request.data.get('movie')
        if not movie_id:
            return Response({'error': 'Movie ID is required'}, status=HTTP_400_BAD_REQUEST)

        history = WatchHistory.objects.create(user=request.user, movie_id=movie_id)
        serializer = WatchHistorySerializer(history)
        return Response(serializer.data, status=HTTP_201_CREATED)

    if request.method == 'GET':
        history = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
        serializer = WatchHistorySerializer(history, many=True)
        print(serializer.data)
        return Response(serializer.data)
     
     
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watch_history_view(request):
    if request.method == 'POST':
        movie_id = request.data.get('movie_id')  # Ensure correct movie ID field
        if not movie_id:
            return Response({'error': 'Movie ID is required'}, status=HTTP_400_BAD_REQUEST)

        # Record the movie click in watch history
        history = WatchHistory.objects.create(user=request.user, movie_id=movie_id)
        serializer = WatchHistorySerializer(history)
        return Response(serializer.data, status=HTTP_201_CREATED)

    if request.method == 'GET':
        history = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
        serializer = WatchHistorySerializer(history, many=True)
        return Response(serializer.data)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response({'error': 'Current and new passwords are required.'}, status=HTTP_400_BAD_REQUEST)

    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect.'}, status=HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'success': 'Password changed successfully.'}, status=HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, id): 
    movie = get_object_or_404(Movie, id=id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data, status=HTTP_200_OK)