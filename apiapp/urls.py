
from django.urls import path
from apiapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.Signup),
    path('login/',  views.login),
    path('movies/', views.movie_list),
    path('watchlist/', views.watchlist_view),
    path('watchhistory/', views.watch_history_view, name='watchhistory'),
    path('changepassword/', views.change_password),
    path('user/', views.user_detail),
    # path('moviedetail/', views.movie_detail),
    path('moviedetail/<int:id>/', views.movie_detail),


]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

