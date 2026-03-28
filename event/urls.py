from django.urls import path
from .views import EventListView,EventRegisterViews,EventStatsView,TopEventsView


urlpatterns = [
    path('event/',EventListView.as_view({'get':'list'}),name='event list'),
    path('event/<int:pk>/register/',EventRegisterViews.as_view()),
    path('event/<int:id>/stats/',EventStatsView.as_view()),
    path('event/top/',TopEventsView.as_view())
]