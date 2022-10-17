from django.urls import path
from . import views

app_name = 'pollapp' # --- this gives our pollapp a namespace. when you make a project with dozens of apps, 
# this enables you to create lots of url paths and namespace each app so django knows which url path to follow. 
# wiring up the routes to display each of the functions in your views.py. 
urlpatterns = [
    # /polls/
    path('', views.IndexView.as_view(), name='index'),
    # /polls/:id/
    path("<int:pk>/", views.DetailView.as_view(), name='detail'),
    # /polls/:id/results/
    # keeping this old line so I can remember how the 'old' 'harder' way is. 
    # path("<int:pk>/results/", views.results, name='results'),
    path("<int:pk>/results/", views.ResultsView.as_view(), name='results'),
    # polls/:id/vote/
    # when I refactored these lines of code, this one didn't change...
    path("<int:question_id>/vote/", views.vote, name='vote')

]