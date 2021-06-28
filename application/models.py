from django.db import models

class hostmain(models.Model):
    hostname=models.CharField(max_length=30,default=None)
    hostemail=models.EmailField(max_length=30,default=None)
    pass1=models.CharField(default=None,max_length=30)
    pass2=models.CharField(default=None,max_length=30)

class users(models.Model):
    hostname=models.CharField(max_length=30,default=None)
    username=models.CharField(max_length=30,default=None)
    useremail=models.EmailField(max_length=30,default=None)
    userpass1=models.CharField(default=None,max_length=30)
    userpass2=models.CharField(default=None,max_length=30)
    attempt=models.BooleanField(default=True)
    score=models.IntegerField(default=-1)

class question(models.Model):
    hostname=models.CharField(max_length=30,default=None)
    question=models.CharField(max_length=1000,default=None)
    option1=models.CharField(max_length=300,default=None)
    option2=models.CharField(max_length=300,default=None)
    option3=models.CharField(max_length=300,default=None)
    option4=models.CharField(max_length=300,default=None)
    rightoption=models.CharField(max_length=300,default=None)
