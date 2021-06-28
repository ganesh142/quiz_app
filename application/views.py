from django.shortcuts import render,redirect
from .models import hostmain,users,question
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'home.html')
def hostreg(request):
    if request.method=='POST':
        hostnm=request.POST['hostnm']
        hostem=request.POST['hostem']
        pass1=request.POST['hostpw1']
        pass2=request.POST['hostpw2']
        if hostnm=='' or hostem=='' or pass1=='' or pass2=='':
            messages.info(request,'please fill all the details')
            return redirect('hostreg')    
        else:
            if pass1==pass2:
                if hostmain.objects.filter(hostname=hostnm).exists():
                    messages.info(request,'hostname already taken')
                    return redirect('hostreg')
                elif hostmain.objects.filter(hostemail=hostem).exists():
                    messages.info(request,'email already taken')
                    return redirect('hostreg')
                else:
                    main=hostmain()
                    main.hostname=hostnm
                    main.hostemail=hostem
                    main.pass1=pass1
                    main.pass2=pass2
                    main.save()
                    return redirect('/')
            else:
                messages.info(request,'passwords did not matching')
                return redirect('hostreg')
    else:
        return render(request,'hostreg.html')
def hostlgn(request):
    if request.method=='POST':
        hostnm=request.POST['hostname']
        passwd=request.POST['pass']
        if hostmain.objects.filter(hostname=hostnm).exists():
            if hostmain.objects.get(hostname=hostnm).pass1==passwd:
                hostlgn.hostname=hostnm
                return render(request,'data.html',{'hostname':hostnm})
            else:
                messages.info(request,'password is incorrect')
                return redirect('hostlgn')

        else:
            messages.info(request,'hostname does not exists')
            return redirect('hostlgn')

    else:
        return render(request,'hostlgn.html')
def userlgn(request):
    if request.method=='POST':
        hostnm=request.POST['hostname']
        usernm=request.POST['username']
        passwd=request.POST['passwd']
        if users.objects.filter(hostname=hostnm,username=usernm,userpass1=passwd).exists():
            if users.objects.filter(hostname=hostnm,username=usernm,userpass1=passwd,attempt=True).exists():
                userlgn.hostname=hostnm
                userlgn.username=usernm
                return render(request,'start.html',{'user':usernm})
            else:
                messages.info(request,'you have already completed the Exam.')
                return redirect('userlgn')    
        else:
            messages.info(request,'record not found')
            return redirect('userlgn')
    else:
        return render(request,'userlgn.html')
def data(request):
    hostnm=hostlgn.hostname
    return render(request,'data.html',{'hostname':hostnm})
def addqn(request):
    if request.method=='POST':
        hostnm=hostlgn.hostname
        q=request.POST['question']
        opt1=request.POST['option1']
        opt2=request.POST['option2']
        opt3=request.POST['option3']
        opt4=request.POST['option4']
        rch=request.POST['right']
        if '' not in (hostnm,q,opt1,opt2,opt3,opt4):
            if hostmain.objects.filter(hostname=hostnm).exists():
                if question.objects.filter(hostname=hostnm,question=q).exists():
                    messages.info(request,'question already exists')
                    return redirect('addqn')
                else:
                    if len({opt1,opt2,opt3,opt4})==4:
                        if rch in (opt1,opt2,opt3,opt4):
                            q=question(hostname=hostnm,question=q,option1=opt1,option2=opt2,option3=opt3,option4=opt4,rightoption=rch)
                            q.save()
                            return redirect('addqn')
                        else:
                            messages.info(request,'right choice should be from your options')
                            return redirect('addqn')
                    else:
                        messages.info(request,'please enter unique options')
                        return redirect('addqn')
            else:
                messages.info(request,'hostname does not exists')
                return redirect('addqn')
        else:
            messages.info(request,'please fill all the details')
            return redirect('addqn')
    else:
        hostnm=hostlgn.hostname
        return render(request,'addqn.html',{'hostname':hostnm})
def delqn(request):
    if request.method=='POST':
        hostnm=hostlgn.hostname
        q=request.POST['question']
        if hostmain.objects.filter(hostname=hostnm).exists():
            if question.objects.filter(hostname=hostnm,question=q).exists():
                q=question.objects.get(hostname=hostnm,question=q)
                q.delete()
                return redirect('delqn')
            else:
                messages.info(request,'question does not exists')
                return redirect('delqn')
        else:
            messages.info(request,'hostname not exists')
            return redirect('delqn')
    else:
        hostnm=hostlgn.hostname
        return render(request,'delqn.html',{'hostname':hostnm})
def addusr(request):
    if request.method=='POST':
        hostnm=hostlgn.hostname
        usernm=request.POST['username']
        userem=request.POST['useremail']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if '' in (hostnm,usernm,userem,pass1,pass2):
            messages.info(request,'please fill all the details')
            return redirect('addusr')
        else:
            if hostmain.objects.filter(hostname=hostnm).exists():
                if users.objects.filter(hostname=hostnm,username=usernm).exists():
                    messages.info(request,'username already given')
                    return redirect('addusr')
                elif users.objects.filter(hostname=hostnm,useremail=userem).exists():
                    messages.info(request,'email already given')
                    return redirect('addusr')
                else:
                    if pass1==pass2:
                        user=users(hostname=hostnm,username=usernm,useremail=userem,userpass1=pass1,userpass2=pass2)
                        user.save()
                        return redirect('addusr')
                    else:
                        messages.info(request,'passwords did not matching')
                        return redirect('addusr')
            else:
                messages.info(request,'hostname does not exists')
                return redirect('addusr')
    else:
        hostnm=hostlgn.hostname
        return render(request,'addusr.html',{'hostname':hostnm})
def delusr(request):
    if request.method=='POST':
        hostnm=hostlgn.hostname
        usernm=request.POST['username']
        if hostmain.objects.filter(hostname=hostnm).exists():
            if users.objects.filter(hostname=hostnm,username=usernm).exists():
                user=users.objects.get(hostname=hostnm,username=usernm)
                user.delete()
                return redirect('delusr')
            else:
                messages.info(request,'username does not exists')
                return redirect('delusr')
        else:
            messages.info(request,'hostname doesnot exists')
            return redirect('delusr')
    else:
        hostnm=hostlgn.hostname
        return render(request,'delusr.html',{'hostname':hostnm})
def start(request):
    return render(request,'start.html')
def exam(request):
    hostnm=userlgn.hostname
    usernm=userlgn.username
    user=users.objects.get(hostname=hostnm,username=usernm)
    user.attempt=False
    user.save()
    host=question.objects.filter(hostname=hostnm)
    return render(request,'exam.html',{'host':host})
def logout(request):
    return redirect('home')
def getscore(request):
    hostnm=userlgn.hostname
    usernm=userlgn.username
    user=users.objects.get(hostname=hostnm,username=usernm)
    if user.score==-1:
        score=0
        q=question.objects.filter(hostname=hostnm)
        list=[k.rightoption for k in q]
        num=q.count()
        for i in range(0,num):
            if list[i]==request.POST[str(i+1)]:
                score=score+1
        user=users.objects.get(hostname=hostnm,username=usernm)
        user.score=score
        user.save()
        return render(request,'score.html',{'score':score,'username':usernm})
    else:
        return render(request,'score.html',{'score':user.score,'username':usernm})

def hostdel(request):
    if request.method=='POST':
        hostnm=request.POST['hostname']
        passwd=request.POST['pass']
        if hostmain.objects.filter(hostname=hostnm).exists():
            main=hostmain.objects.get(hostname=hostnm)
            if main.pass1==passwd:
                main.delete()
                user=users.objects.filter(hostname=hostnm)
                for u in user:
                    u.delete()
                que=question.objects.filter(hostname=hostnm)
                for q in que:
                    q.delete()
                return redirect('home')
            else:
                messages.info(request,'password is incorrect')
                return redirect('hostdel')
        else:
            messages.info(request,'hostname does not exists')
            return redirect('hostdel')
    else:
        return render(request,'hostdel.html')

def qlst(request):
    hostnm=hostlgn.hostname
    que=question.objects.filter(hostname=hostnm)
    n=que.count()
    return render(request,'qlst.html',{'que':que,'n':n,'hostname':hostnm})
def ulst(request):
    hostnm=hostlgn.hostname
    user=users.objects.filter(hostname=hostnm)
    num=user.count()
    return render(request,'ulst.html',{'user':user,'num':num,'hostname':hostnm})
def updtq(request):
    hostnm=hostlgn.hostname
    if request.method=='POST':
        que=request.POST['que']
        quenew=request.POST['quenew']
        opt1=request.POST['option1']
        opt2=request.POST['option2']
        opt3=request.POST['option3']
        opt4=request.POST['option4']
        rch=request.POST['rtch']
        if '' in (quenew,opt1,opt2,opt3,opt4,rch):
            messages.info(request,'please fill all the details')
            return redirect('updtq')
        else:
            if question.objects.filter(hostname=hostnm,question=que).exists():
                if len({opt1,opt2,opt3,opt4})==4:
                    if rch in (opt1,opt2,opt3,opt4):
                        if question.objects.filter(hostname=hostnm,question=quenew).exists() and que!=quenew:
                                messages.info(request,'question already exists')
                                return redirect('updtq')
                        else:
                            q=question.objects.get(hostname=hostnm,question=que)
                            q.question=quenew
                            q.option1=opt1
                            q.option2=opt2
                            q.option3=opt3
                            q.option4=opt4
                            q.rightoption=rch
                            q.save()
                            return redirect('updtq')
                    else:
                        messages.info(request,'right option should be from your options')
                        return redirect('updtq')
                else:
                    messages.info(request,'options should be unique')
                    return redirect('updtq')
            else:
                messages.info(request,'question does not exists')
                return redirect('updtq')

    else:
        return render(request,'updtq.html',{'hostname':hostnm})
def upusr(request):
    hostnm=hostlgn.hostname
    if request.method=='POST':
        usernm=request.POST['username']
        usernew=request.POST['usernew']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if '' in (usernew,email,pass1,pass2):
            messages.info(request,'please fill all the details')
            return redirect('upusr')
        else:
            if users.objects.filter(hostname=hostnm,username=usernm).exists():
                user=users.objects.get(hostname=hostnm,username=usernm)
                if users.objects.filter(hostname=hostnm,username=usernew).exists() and usernm!=usernew:
                    messages.info(request,'username already taken')
                    return redirect('upusr')
                elif users.objects.filter(hostname=hostnm,useremail=email).exists() and user.useremail!=email:
                    messages.info(request,'Email already taken')
                    return redirect('upusr')
                elif pass1!=pass2:
                    messages.info(request,'passwords did not matching')
                    return redirect('upusr')
                else:
                    
                    user.username=usernew
                    user.useremail=email
                    user.userpass1=pass1
                    user.userpass2=pass2
                    user.save()
                    return redirect('upusr')
            else:
                messages.info(request,'username does not exists')
                return redirect('upusr')

    else:
        return render(request,'upusr.html',{'hostname':hostnm})
def chnm(request):
    hostnm=hostlgn.hostname
    if request.method=='POST':
        newhostnm=request.POST['newhostnm']
        passwd=request.POST['passwd']
        if hostnm==newhostnm:
            messages.info(request,'new hostname has no changes')
            return redirect('chnm')
        elif hostmain.objects.filter(hostname=newhostnm).exists():
            messages.info(request,'hostname already taken')
            return redirect('chnm')
        else:
            main=hostmain.objects.get(hostname=hostnm)
            user=users.objects.filter(hostname=hostnm)
            que=question.objects.filter(hostname=hostnm)
            if main.pass1==passwd:
                user=users.objects.filter(hostname=hostnm)
                que=question.objects.filter(hostname=hostnm)
                main.hostname=newhostnm
                hostlgn.hostname=newhostnm
                main.save()
                for u in user:
                    u.hostname=newhostnm
                    u.save()
                for q in que:
                    q.hostname=newhostnm
                    q.save()
                return redirect('chnm')
            else:
                messages.info(request,'password is incorrect')
                return redirect('chnm')
    else:
        return render(request,'chnm.html',{'hostname':hostnm})
def chml(request):
    hostnm=hostlgn.hostname
    if request.method=='POST':
        newhostml=request.POST['newhostml']
        passwd=request.POST['passwd']
        if hostmain.objects.get(hostname=hostnm).hostemail==newhostml:
            messages.info(request,'new hostemail has no changes')
            return redirect('chml')
        elif hostmain.objects.filter(hostname=hostnm,hostemail=newhostml).exists():
            messages.info(request,'hostemail already taken')
            return redirect('chml')
        else:
            main=hostmain.objects.get(hostname=hostnm)
            if main.pass1==passwd:
                main.hostemail=newhostml
                main.save()
                return redirect('chml')
            else:
                messages.info(request,'password is incorrect')
                return redirect('chml')
    else:
        return render(request,'chml.html',{'hostname':hostnm})
def chpw(request):
    hostnm=hostlgn.hostname
    if request.method=='POST':
        oldpass=request.POST['oldpass']
        newpass1=request.POST['newpass1']
        newpass2=request.POST['newpass2']
        if hostmain.objects.get(hostname=hostnm).pass1!=oldpass:
            messages.info(request,'old password is incorrect')
            return redirect('chpw')
        elif oldpass==newpass1:
            messages.info(request,'new password has no changes')
            return redirect('chpw')
        elif newpass1!=newpass2:
            messages.info(request,'passwords did not matching')
            return redirect('chpw')
        else:
            main=hostmain.objects.get(hostname=hostnm)
            main.pass1=newpass1
            main.pass2=newpass2
            main.save()
            return redirect('chpw')
            
    else:
        return render(request,'chpw.html',{'hostname':hostnm})