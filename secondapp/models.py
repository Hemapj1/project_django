from django.db import models

# Create your models here.
class Problems(models.Model):
    problemname=models.CharField(max_length=100)
    problemcode=models.CharField(max_length=100)
    problemstatement=models.CharField(max_length=100)
    def __str__(self):
        return self.problemname

class Testcases(models.Model):
    input=models.CharField(max_length=100)
    output=models.CharField(max_length=100)
    problem=models.ForeignKey(Problems,on_delete=models.CASCADE)

