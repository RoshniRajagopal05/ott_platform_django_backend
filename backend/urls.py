from django.contrib import admin
from django.urls import include, path
from adminapp import views
from django.conf import settings
from django.conf.urls.static import static


  
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.admin_login, name="adminlogin"),
    path('movie-list/', views.movie_list, name='movielist'),
    path('user-listing/', views.users_list, name='userlisting'),
    path('change-password/', views.change_password, name='changepassword'),  
    path('add-movie/', views.add_movie, name='addmovie'),
    path('movie-edit/<int:id>/', views.movie_edit, name='movieedit'),
    path('movie-view/<int:id>/', views.movie_view, name='movieview'),
    path('movie-delete/<int:id>/', views.movie_delete, name='moviedelete'),
    path('watch-history/<int:user_id>/', views.watch_history, name='watchhistory'),
    path('reports/', views.reports, name='reports'),
    path('api/', include('apiapp.urls')),
   
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)