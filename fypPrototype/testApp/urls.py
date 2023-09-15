
from django.urls import path
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf import settings

urlpatterns = [
    #landing page
    path('', Index.as_view(), name='index'),
    #pages
    #home
    path('home/', login_required(login_url=settings.BASE_URL+'login/')(Exercise.as_view()), name='home'),
    #mark-as-completed
    path('home/mark-complete/', login_required(login_url=settings.BASE_URL+'login/')(MarkComplete.as_view()), name='mark-complete'),
    #leadership-board
    path('board/', login_required(login_url=settings.BASE_URL+'login/')(Board.as_view()), name='board'),
    #profile
    path('profile/<int:pk>/', login_required(login_url=settings.BASE_URL+'login/')(ProfileView.as_view()), name='profile'),
    path('profile/<int:pk>/following/add/', login_required(login_url=settings.BASE_URL+'login/')(Follow.as_view()), name='follow'),
    path('profile/<int:pk>/following/remove/', login_required(login_url=settings.BASE_URL+'login/')(RemoveFollow.as_view()), name='remove-follow'),
    #settings
    path('settings/', login_required(login_url=settings.BASE_URL+'login/')(Settings.as_view()), name='settings'),
    #search
    path('search/', SearchProfile.as_view(), name='search-profile'),
    #authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
