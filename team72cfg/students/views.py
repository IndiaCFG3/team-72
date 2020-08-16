from django.shortcuts import render,redirect
from .models import Student
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, UserDataForm
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

@login_required
def register(request):
    context ={}
    form = StudentRegistrationForm(request.POST or None, request.FILES or None)
    t=Teacher.objects.get(id=request.user.id)
    form.instance.teacher=t
    if form.is_valid(): 
        form.save() 
        username=form.cleaned_data.get('firstname')
        messages.success(request,f'{username} registered !!')
        return redirect('home')
    context['form']= form 
    return render(request,'students/register.html',context) 

@login_required
def details(request,id,sid):
    if request.user.id==id:
        if request.method=='POST':
            form=UserDataForm(request.POST)
            s=Student.objects.get(id=sid)
            #t=User.objects.get(id=id)
            form.instance.student=s
            if form.is_valid(): 
                form.save() 
                messages.success(request,f'Done')
                return redirect('details', id=id, sid=sid)
        else:
            form=UserDataForm()
        return render(request, 'students/details.html',{'form':form})
    else:
        return render(request, 'students/error.html')


