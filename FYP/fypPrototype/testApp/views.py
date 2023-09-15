from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .models import *
from .forms import *
import datetime
from django.db.models import Q
#To authenticate users:
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# landing page
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'landing/index.html')

# Home/exercise page
class Exercise(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        today_date = datetime.date.today()
        today_day = today_date.strftime("%a")
        if(today_date.isoweekday()==7):
            start_week = today_date - datetime.timedelta(7-today_date.isoweekday())
        else:
            start_week = today_date - datetime.timedelta(today_date.isoweekday())
        end_week = start_week + datetime.timedelta(6)
        if(start_week.strftime("%B") != end_week.strftime("%B")):
            month = start_week.strftime("%B")+'-'+end_week.strftime("%B")
        else:
            month = start_week.strftime("%B")
        completed_dates = Completed_Dates.objects.filter(user=current_user.id).order_by('-date')[:7].values()
        exercise_day = Exercise_Day.objects.filter(user=current_user.id).values()[0]
        show_video = [False]*7
        button_settings = [False]*7
        for i in range(7):
            #past
            if(((start_week+datetime.timedelta(i)) < today_date)):
                for dates in completed_dates:
                    if((start_week+datetime.timedelta(i)) == dates['date']):
                        show_video[i]=True
                        if(dates['completed']):
                            button_settings[i]=True
                            break
                        break
            #present
            elif((start_week+datetime.timedelta(i)) == today_date):
                for dates in completed_dates:
                    if((start_week+datetime.timedelta(i)) == dates['date']):
                        show_video[i]=True
                        if(dates['completed']):
                            button_settings[i]=True
                            break
                        break
                if(exercise_day[((start_week+datetime.timedelta(i)).strftime("%a")).lower()]):
                    show_video[i]=True
            #future
            elif((start_week+datetime.timedelta(i)) > today_date):
                if(exercise_day[((start_week+datetime.timedelta(i)).strftime("%a")).lower()]):
                    show_video[i]=True
        days = {}
        shows = {}
        for i in range(7):
            days.update({(start_week+datetime.timedelta(i)).strftime("%a"): (start_week+datetime.timedelta(i)).strftime("%d")})
            shows.update({(start_week+datetime.timedelta(i)).strftime("%a"): (show_video[i], button_settings[i])})
        #print('/////////////////////////////////////////////////')
        #print(shows)
        context = {
            'today_day': today_day,
            'month': month,
            'days': days,
            'shows': shows,
        }
        return render(request, 'pages/exercise.html', context)

#To mark as complete
class MarkComplete(View):
    def post(self, request, *args, **kwargs):
        #to post data to completed_dates
        current_user = request.user
        today_date = datetime.date.today()
        Completed_Dates.objects.create(user=current_user, completed=True, date=today_date)
        profile = Profile.objects.get(user=current_user)
        current_streak = profile.current_streak
        highest_streak = profile.highest_streak
        Profile.objects.filter(user=current_user).update(current_streak=(current_streak+1))
        #print('/////////////////////////////')
        #print(current_streak)
        #print(highest_streak)
        if(current_streak+1>highest_streak):
            Profile.objects.filter(user=current_user).update(highest_streak=(current_streak+1))
        #note: since this is an offline case, there will not be checking for incompleted
        #workout days (as this is done in online server side). In the real implementation,
        #completed_dates data wil be inserted daily and if the user missed a day, the
        #current_streak will reset to 0. (In this case, I will insert data manually to
        #replicate the "intended" outcome instead).
        #get content
        return redirect('home')

# Profile page
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        current_user = Profile.objects.get(user=request.user)
        following_list = current_user.following.all()

        if len(following_list) == 0:
            is_following = False
        
        for following in following_list:
            if following == user:
                is_following = True
                break
            else:
                is_following = False
        
        context = {
            'profile': profile,
            'user': user,
            'is_following': is_following,
        }
        print(is_following)
        return render(request, 'pages/profile.html', context)

#To follow
class Follow(View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        current_profile = Profile.objects.get(user=request.user)
        current_profile.following.add(User.objects.get(pk=pk))
        print(User.objects.get(pk=pk))
        return redirect('profile', pk=profile.pk)

#To remove follow
class RemoveFollow(View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        current_profile = Profile.objects.get(user=request.user)
        current_profile.following.remove(User.objects.get(pk=pk))
        print(User.objects.get(pk=pk))
        return redirect('profile', pk=profile.pk)

#Search page
class SearchProfile(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(
            Q(user__username__icontains=query)
        )
        current_user = Profile.objects.get(user=request.user)
        following_list = current_user.following.all()
        is_following = {}
        for i in range(len(profile_list)):
            for follow in following_list:
                if(profile_list[i].user == follow):
                    is_following.update({str(profile_list[i].user): True})
                else:
                    is_following.update({str(profile_list[i].user): False})
        print('//////////////////')
        print(is_following)
        context = {
            'profile_list': profile_list,
            'following_list': following_list,
        }
        return render(request, 'pages/search.html', context)

#Settings page
class Settings(View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = UserProfileForm()
        exercise_form = ExerciseDayForm()
        current_profile = Profile.objects.get(user=request.user)
        context = {'user_form': user_form,
                    'profile_form': profile_form,
                    'exercise_form': exercise_form,
                    'profile': current_profile,
        }
        return render(request, 'authentication/settings.html', context)
    
    def post(self, request, *args, **kwargs):
        current_profile = Profile.objects.get(user=request.user)
        current_user = User.objects.get(pk=current_profile.pk)
        user_form = SettingUserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        exercise_form = ExerciseDayForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid() and exercise_form.is_valid():
            current_user.email = user_form.cleaned_data.get("email")
            current_user.save()
            profile = profile_form.save(commit=False)
            profile.user = current_user
            profile.current_streak = current_profile.current_streak
            profile.highest_streak = current_profile.highest_streak
            profile.profile_image = current_profile.profile_image
            profile.following.set(current_profile.following.all())
            profile.save()
            exercise = exercise_form.save(commit=False)
            exercise.user = current_user
            exercise.save()
        return redirect('profile', pk=current_profile.pk)

class Board(View):
    def get(self, request, *args, **kwargs):
        current_user = Profile.objects.get(user=request.user)
        following_list = current_user.following.all()
        board_items = {}
        for i in range(len(following_list)+1):
            if(i==len(following_list)):
                board_items.update({current_user: current_user.current_streak})
            else:
                following=Profile.objects.get(user=following_list[i])
                board_items.update({following: following.current_streak})
        sorted_board_items = dict(sorted(board_items.items(), key=lambda x:x[1], reverse=True))
        board_list = {}
        for i in range(len(sorted_board_items)):
            if(i==0):
                rank=i+1
                board_list.update({i: (rank, str(list(sorted_board_items.keys())[i].profile_image), list(sorted_board_items.keys())[i].pk, str(list(sorted_board_items.keys())[i].user), list(sorted_board_items.keys())[i].name, list(sorted_board_items.keys())[i].current_streak)})
                prev=list(sorted_board_items.keys())[i].current_streak
            elif(prev==list(sorted_board_items.keys())[i].current_streak):
                #dont increase rank, same rank as prev
                board_list.update({i: (rank, str(list(sorted_board_items.keys())[i].profile_image), list(sorted_board_items.keys())[i].pk, str(list(sorted_board_items.keys())[i].user), list(sorted_board_items.keys())[i].name, list(sorted_board_items.keys())[i].current_streak)})
            else:
                rank+=1
                board_list.update({i: (rank, str(list(sorted_board_items.keys())[i].profile_image), list(sorted_board_items.keys())[i].pk, str(list(sorted_board_items.keys())[i].user), list(sorted_board_items.keys())[i].name, list(sorted_board_items.keys())[i].current_streak)})
                prev=list(sorted_board_items.keys())[i].current_streak
        print(following_list)
        print(board_list)
        context = {
            'board_list': board_list,
        }
        return render(request, 'pages/board.html', context)

#To sign up
def signup(request):
    #initially false
    signed_up = False

    #User send us data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        exercise_form = SignUpExerciseForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid() and exercise_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            exercise = exercise_form.save(commit=False)
            exercise.user = user
            exercise.save()
            signed_up = True
    else: #if request.method is not 'POST' show user a blank form
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'authentication/signup.html', {'user_form': user_form,
                                                          'profile_form': profile_form,
                                                          'signed_up': signed_up})

#To login
def login_user(request):
    login_form = LoginForm(request.POST or None)
    if request.POST and login_form.is_valid():
        user = login_form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect("../home/")# Redirect to a success page.
    return render(request, 'authentication/login.html', {'login_form': login_form })

#To logout
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('../')
