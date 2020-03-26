from django.urls.conf import path, re_path

from polls.api.views.questions import (
    QuestionView,
    QuestionChoicesView,
    QuestionChoicesDetailView,
    QuestionDetailView,
    VotesView
)

urlpatterns = [
    path('questions/', QuestionView.as_view()),
    re_path(r'^questions/(?P<id>[0-9])/$', QuestionDetailView.as_view()),
    re_path(r'^questions/(?P<id>[0-9])/choices/$', QuestionChoicesView.as_view()),
    re_path(r'^questions/(?P<id>[0-9])/choices/(?P<choice_id>[0-9])/$', QuestionChoicesDetailView.as_view()),
    re_path(r'^questions/(?P<id>[0-9])/choices/(?P<choice_id>[0-9])/vote/$', VotesView.as_view()),
]
