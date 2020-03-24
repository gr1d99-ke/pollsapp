from django.urls.conf import path, re_path

from .apiviews import QuestionView, QuestionDetailView

urlpatterns = [
    path('questions/', QuestionView.as_view()),
    re_path(r'^questions/(?P<id>[0-9])/$', QuestionDetailView.as_view())
]