from django.shortcuts import render
from .models import Student
from django.contrib.auth.models import User
# Create your views here.
def mystudents(request, id):
    print(id)
    t=User.objects.filter(id=id).first()
    print(t)
    st=Student.objects.filter(teacher=t)
    print(st)
    return render(request, 'students/mystudents.html',{'st':st})