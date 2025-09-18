from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=20)
    viewPassword=models.CharField(max_length=200,null=True)
    

    
class Student_reg(models.Model):
    logid= models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
    Username=models.CharField(max_length=20)
    Email=models.EmailField(unique=True )
    Phonenumber=models.IntegerField()
    Password=models.CharField(max_length=20,null=True)
    Image=models.ImageField(upload_to="Image",null=True)
    Address=models.CharField(max_length=200,null=True)
    Dept=models.CharField(max_length=200,null=True)
    Year=models.CharField(max_length=200,null=True)
    # gid = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, default='Pending')
    

  