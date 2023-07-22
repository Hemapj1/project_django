from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from secondapp.models import Problems,Testcases
# Create your models here.


CustomUser = get_user_model()
class Submissions(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    problem = models.ForeignKey(Problems, null=True, on_delete=models.SET_NULL)
    verdict = models.CharField(max_length=100, default="Wrong Answer")
    submission_time = models.DateTimeField(auto_now_add=True, null=True)
    language=models.CharField(max_length=100, default="")


