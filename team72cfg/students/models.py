from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Student(models.Model):
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    email=models.EmailField()
    phone = models.CharField(max_length=12)
    teacher=models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    keywords=models.TextField()

    def __str__(self):
        return self.firstname+" "+self.lastname

class Skill(models.Model):
    mainskill=models.CharField(max_length=30)
    subskill=models.CharField(max_length=50)
    skillnames=models.CharField(max_length=100)
    

    def __str__(self):
        return self.mainskill+"->"+self.subskill + "->"+self.skillnames

class Skillset(models.Model):
    yn=models.BooleanField(verbose_name="Yes or No")
    comment=models.CharField(max_length=100)
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    skills=models.ForeignKey(Skill,on_delete=models.CASCADE)
    time_posted=models.TimeField(default=timezone.now)

    def __str__(self):
        return self.skills.skillnames+" "+self.student.firstname 