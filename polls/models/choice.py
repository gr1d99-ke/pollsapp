from django.db import models

from tenants.models import TenantAwareModel

from .question import Question


class Choice(TenantAwareModel):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
