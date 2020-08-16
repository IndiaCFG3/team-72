from django.shortcuts import render
from .models import Student
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def mystudents(request, id):
    if request.user.id==id:
        print(id)
        t=User.objects.filter(id=id).first()
        print(t)
        st=Student.objects.filter(teacher=t)
        print(st)
        return render(request, 'students/mystudents.html',{'st':st})
    else:
        return render(request, 'students/error.html')