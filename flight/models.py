from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(primary_key=True,max_length=30)
    password=models.CharField(max_length=10,null=False)
    name=models.CharField(max_length=30,null=False)
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    fathers_name=models.CharField(max_length=30,default='')
    mothers_name=models.CharField(max_length=30,default='')
    phone=models.CharField(max_length=10,default='')
    email=models.CharField(max_length=30,default='')
    address=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.username

class flights_from_to(models.Model):
    from_from=models.CharField(max_length=30)
    to_to=models.CharField(max_length=30)
    flight=models.CharField(max_length=30)
    date=models.CharField(max_length=30, default='')
    def __str__(self):
        return self.from_from
    
class fare(models.Model):
    flight=models.CharField(max_length=30)
    flight_class=models.CharField(max_length=30)
    flight_fare=models.CharField(max_length=30)
    def __str__(self):
        return self.flight
    
