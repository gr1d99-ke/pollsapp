from django.urls.conf import path, re_path

from polls.api.views.questions import (
    QuestionView,
    QuestionChoicesView,
    QuestionChoicesDetailView,
    QuestionDetailView,
    VotesView
)

from polls import views

api_urls = [
    path('api/questions/', QuestionView.as_view()),
    re_path(r'^api/questions/(?P<id>[0-9])/$', QuestionDetailView.as_view()),
    re_path(r'^api/questions/(?P<id>[0-9])/choices/$', QuestionChoicesView.as_view()),
    re_path(r'^api/questions/(?P<id>[0-9])/choices/(?P<choice_id>[0-9])/$', QuestionChoicesDetailView.as_view()),
    re_path(r'^api/questions/(?P<id>[0-9])/choices/(?P<choice_id>[0-9])/vote/$', VotesView.as_view()),
]

app_name = 'polls'

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]

urlpatterns = urlpatterns + api_urls
