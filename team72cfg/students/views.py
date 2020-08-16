from django.shortcuts import render,redirect
from .models import Student, Skill, Skillset
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, UserDataForm
import requests
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
def detailsform(request,id,sid):
    if request.user.id==id:
        if request.method=='POST':
            form=UserDataForm(request.POST)
            s=Student.objects.get(id=sid)
            #t=User.objects.get(id=id)
            form.instance.student=s
            if form.is_valid(): 
                form.save() 
                messages.success(request,f'Done')
                return redirect('details-form', id=id, sid=sid)
        else:
            form=UserDataForm()
        return render(request, 'students/detailsform.html',{'form':form,'sid':sid})
    else:
        return render(request, 'students/error.html')


def details(request,id,sid):
    if request.user.id==id:
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        li=[]
        s1=Skill.objects.all()
        for s in s1:
            if s.mainskill not in li:
                li.append(s.mainskill)
        
        li3=[]
        for i in li:
            li2=[]
            for s in Skillset.objects.all():
                if s.skills.mainskill==i and s.student.id==sid:
                    li2.append(s.comment)
            li3.append(li2)
        
        diction={'skills':str(li),'comments':str(li3)}
        response=requests.post('http://127.0.0.1:5000/comments/keywords',data=diction)
        print(response.json())
        keywords=response.json()
        

        lif={}
        lif2=[]
        for i in li:
            count=0
            for s in Skill.objects.filter(mainskill=i):
                #c=Skillset.objects.filter(skill.subskill=s.subskill).count()
                c=0
                for sn in Skill.objects.filter(mainskill=i):
                    if(sn.subskill==s.subskill):
                        c=c+1
                y=0
                for sk in Skillset.objects.all():
                    if sk.yn==True and sk.student.id==sid and sk.skills.subskill==s:
                        y=y+1
                count=count+y/c
            count=count/len(li)
            lif2.append(count)
            lif[i]=count


        print(lif)
        min=100
        for i in lif2:
            if i<min:
                min=i

        diction={'skills':str(li),'comments':str(li3),'points':str(lif)}
        response2=requests.post('http://127.0.0.1:5000/comments/sentiment',data=diction)
        print(response2.json())
        x=response2.json()
        t=list(x.values())
        #minimum=min(t)
        #keymin=[ key for key in x if x[key]==minimum]
        return render(request, 'students/details.html',{'sid':sid,'x':x,'keywords':keywords})
    else:
        return render(request, 'students/error.html')


