

from django.shortcuts import render, redirect,get_object_or_404
from apiapp.models import Movie, WatchHistory 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from apiapp.models import User
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_superuser or user.is_admin:  
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('movielist')
            else:
                messages.error(request, "You are not authorized as admin.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'adminlogin.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, "Password changed successfully.")
        return redirect('adminlogin.html')
    return render(request, 'changepassword.html') 



@login_required
def movie_list(request):
    query = request.GET.get('q', '')  
    movies = Movie.objects.filter(title__icontains=query) if query else Movie.objects.all()
    
    return render(request, 'movielist.html', {'movies': movies, 'query': query})



@login_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video = request.FILES.get('video')
        thumbnail = request.FILES.get('thumbnail')

        
        Movie.objects.create(
            title=title,
            description=description,
            video=video,
            thumbnail=thumbnail
        )

        messages.success(request, "Movie added successfully.")
        return redirect('movielist')  

    return render(request, 'add_movie.html')  


def movie_edit(request, id):
    movie = get_object_or_404(Movie, id=id)  
    
    if request.method == 'POST':
        movie.title = request.POST.get('title', movie.title)
        movie.description = request.POST.get('description', movie.description)
        
        if 'video' in request.FILES:
            movie.video = request.FILES['video']
            
        if 'thumbnail' in request.FILES:
            movie.thumbnail = request.FILES['thumbnail']
        
        movie.save()
        return redirect('movielist') 

    return render(request, 'movie_edit.html', {'movie': movie}) 



def movie_view(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'movie_view.html', {'movie': movie})



def movie_delete(request, id):
    movie = get_object_or_404(Movie, id=id)
    
    if request.method == 'POST':
        movie.delete()
        return redirect('movielist')
    
    return render(request, 'movie_delete.html', {'movie': movie})


@login_required    
def users_list(request):
    query = request.GET.get('q')

    if query:
        users = User.objects.filter(email__icontains=query, is_admin=False, is_superuser=False)  # Exclude admins & superusers
    else:
        users = User.objects.filter(is_admin=False, is_superuser=False)  # Fetch only regular users
    
    return render(request, 'user_list.html', {'users': users})


@login_required
def watch_history(request, user_id):
    user = get_object_or_404(User, id=user_id)  
    history = WatchHistory.objects.filter(user=user)  
    
    return render(request, 'watch_history.html', {'user': user, 'history': history})




@login_required
def reports(request):
    query = request.GET.get('q', '')  

    movie_reports = WatchHistory.objects.values('movie__id', 'movie__title').annotate(
        total_views=Count('movie')
    ).order_by('-total_views')

    if query:
        movie_reports = movie_reports.filter(Q(movie__title__icontains=query))

    return render(request, 'reports.html', {'movie_reports': movie_reports, 'query': query})

