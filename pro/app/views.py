from django.shortcuts import render,redirect
from .models import user,item,cart,order,PasswordReset
from django.http import  HttpResponse,HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime, timedelta
import re,razorpay


def ind(request):
    return render(request,'index.html')

def log(request):
    if request.method=='POST':
        un=request.POST['un']
        p=request.POST['p']
        try:
            data2=user.objects.get(uname=un)
            if(data2.uname=="admin"):
                if(data2.pas==p):
                    request.session['aid']=un
                    return redirect(adash)
                else:
                    messages.error(request, "incorrect username or password")
                    return render(request, 'login.html')
            else:
                 if (data2.pas == p):
                    request.session['uid'] = un
                    return redirect(ds)
                 else:
                     messages.error(request, "incorrect username or password ")
                     return render(request, 'login.html')
        except Exception:
            messages.error(request,'incorrect username or password ')
            return render(request, 'login.html')
    else:
        return render(request,'login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            us = user.objects.get(eml=email)
        except:
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
            # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=us, token=token)

            # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                          'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request, 'frgt.html')


def reset_password(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.pas=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(log)
    return render(request, 'rest-pass.html',{'token':token})

def reg(request):
    if request.method=='POST':
        un = request.POST['un']
        a = request.POST['a']
        e = request.POST['e']
        ph = request.POST['ph']
        p = request.POST['p']
        try:
            if user.objects.filter(uname=un).exists():
                messages.error(request,"user already exist")
            elif len(ph)!=10:
                messages.error(request,"phone number must contain 10 digits")
            elif user.objects.filter(eml=e).exists():
                messages.error(request,"This email already exits")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',e):
                messages.error(request,"Enter valid email")
            elif len(p) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
            else:
                data=user.objects.create(uname=un,adrs=a,eml=e,phn=ph,pas=p)
                data.save()
                return render(request, 'login.html',{'d':data})
        except Exception:
            messages.error(request,'Problem in Registration ')
            return render(request, 'register.html')
    return render(request,'register.html')
def bk(request):
    return render(request,'index.html')
def adash(request):
    if 'aid' in request.session:
        return render(request,'adash.html')
    return redirect(log)

def pro(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        data = user.objects.get(uname=uid)
        return render(request, 'profile.html', {'i': data})
    else:
        return redirect(log)
def upd(request):
    if 'uid' in request.session:
        if(request.method=='POST'):
            un = request.POST['un']
            a = request.POST['a']
            e = request.POST['e']
            ph = request.POST['ph']
            p = request.POST['p']
            d = user.objects.filter(uname=un)
            d.update(uname=un,adrs=a,eml=e,phn=ph,pas=p)
            return redirect(pro)
        else:
            return redirect(pro)
    return redirect(log)

def apro(request):
     if 'aid' in request.session:
        aid = request.session['aid']
        data = user.objects.get(uname=aid)
        return render(request, 'aprof.html', {'i': data})
     else:
         return redirect(log)
def aupd(request):
    if 'aid' in request.session:
        if (request.method == 'POST'):
            un = request.POST['un']
            a = request.POST['a']
            e = request.POST['e']
            ph = request.POST['ph']
            p = request.POST['p']
            d = user.objects.filter(uname=un)
            d.update(uname=un, adrs=a, eml=e, phn=ph, pas=p)
            return redirect(apro)
        else:
            return redirect(apro)
    else:
        return redirect(log)

def logouta(request):
    if 'aid' in request.session:
        request.session.flush()
        return redirect(log)


def adi(request):
    if 'aid' in request.session:
        if request.method=='POST':
            itn = request.POST['tn']
            im = request.POST['im']
            r = request.POST['r']
            qt = request.POST['qt']
            data=item.objects.create(image=im,iname=itn,rate=r,qty=qt,prate=r)
            data.save()
            d = item.objects.all()
            return render(request, 'adpt.html',{'data': d})
        else:
            d = item.objects.all()
            return render(request, 'adpt.html',{'data': d})
    return redirect(log)
def upi(request):
    if 'aid' in request.session:
        data = item.objects.all()
        return render(request,'uptyp.html',{'d':data})
    return redirect(log)
def deli(request,id):
    if 'aid' in request.session:
        data = item.objects.filter(iid=id)
        data.delete()
        return redirect(upi)
    return redirect(log)
def edi(request,id):
    if 'aid' in request.session:
        data = item.objects.filter(iid=id)
        return render(request, 'edtyp.html',{'d': data})
    return redirect(log)

def itup(request,id):
    if 'aid' in request.session:
        if (request.method == 'POST'):
            iid=request.POST['iid']
            itn = request.POST['tn']
            r = request.POST['r']
            qt = request.POST['qt']
            d = item.objects.filter(iid=id)
            d.update(iid=iid,iname=itn,rate=r,qty=qt)
            return redirect(upi)
        else:
            return redirect(upi)
    return redirect(log)

def ds(request):
    if 'uid' in request.session:
        us = user.objects.get(uname=request.session['uid'])
        data=user.objects.all()
        datas = cart.objects.filter(uid=us)
        print(data)
        return render(request,'dash.html',{'d':data,'d1':datas})
    return redirect(log)
def ordr(request):
    if 'uid' in request.session:
        us = user.objects.get(uname=request.session['uid'])
        l = []
        datas = ''
        try:
            datas = cart.objects.filter(uid=us)
            d1 = datas
            print(datas)
            for i in datas:
                l.append(i.iid)
        except:
            pass
        data = item.objects.all()
        print(l)
        return render(request, 'order.html', {'data': data, 'datas': l, 'd1': d1})
    return redirect(log)

def abst(request):
    if 'uid' in request.session:
        us = user.objects.get(uname=request.session['uid'])
        l = []
        datas = ''
        try:
            datas = cart.objects.filter(uid=us)
            d1 = datas
            print(datas)
            for i in datas:
                l.append(i.iid)
        except:
            pass
        data = item.objects.filter(iname='Abstract')
        print(l)
        return render(request, 'abstract.html', {'data': data, 'datas': l, 'd1': d1})
    return redirect(log)
def digi(request):
    if 'uid' in request.session:
        us = user.objects.get(uname=request.session['uid'])
        l = []
        datas = ''
        try:
            datas = cart.objects.filter(uid=us)
            d1 = datas
            print(datas)
            for i in datas:
                l.append(i.iid)
        except:
            pass
        data = item.objects.filter(iname='Digital portrait')
        print(l)
        return render(request, 'digital.html', {'data': data, 'datas': l, 'd1': d1})
    return redirect(log)

def pencl(request):
    if 'uid' in request.session:
        us = user.objects.get(uname=request.session['uid'])
        l = []
        datas = ''
        try:
            datas = cart.objects.filter(uid=us)
            d1 = datas
            print(datas)
            for i in datas:
                l.append(i.iid)
        except:
            pass
        data = item.objects.filter(iname='pencil')
        print(l)
        return render(request, 'pencil.html', {'data': data, 'datas': l, 'd1': d1})
    return redirect(log)


def cart1(request):
    if 'uid' in request.session:
        us = user.objects.get(uname=request.session['uid'])
        datas = cart.objects.filter(uid=us)
        print(datas,us)
        return render(request,'cart.html',{'d1':datas})
    return redirect(log)

def addcart(request,id):
    if 'uid' in request.session:
        u=user.objects.get(uname=request.session['uid'])
        print(u)
        itm=item.objects.get(pk=id)
        print(itm)
        if itm.qty>0:
            if itm.qty < 10:
                z = 'ayiraarts@gmail.com'
                email_message = f" The product {itm.iname} is falling out off stock. its only {itm.qty}, updatae fastly , its high on demand."
                send_mail('ALERT...UPDATE STOCK...', email_message, 'settings.EMAIL_HOST_USER', [z],fail_silently=False)
            data=cart(iid=itm,uid=u,trate=itm.rate)
            data.save()
            messages.success(request,'Cart added successfully')
            return redirect(ditm)
        else:
            msg = "product out of stock"
            print(msg)
        return redirect(ditm,msg)
    return redirect(log)

def ditm(request):
    if 'uid' in request.session:
        u=user.objects.get(uname=request.session['uid'])
        c = cart.objects.filter(uid=u)
        b=cart.objects.filter(uid=u)
        total=0
        for i in b:
            total+=i.iid.rate*i.cqty
        return render(request,'dsitm.html',{'data':b,'total':total,'d1':c})
    return redirect(log)


def inqty(request, id):
    if 'uid' in request.session:
        citem = cart.objects.get(pk=id)
        if citem.iid.qty > 1:
                citem.cqty += 1
                citem.save()
                citem.trate += citem.iid.rate
                citem.save()
        else:
            messages.error(request,'product out of stock')
    return redirect(ditm)


def dcqty(request, id):
    if 'uid' in request.session:
        citem = cart.objects.get(pk=id)
        if citem.iid.qty > 1:
            if citem.cqty>1:
                citem.cqty -= 1
                citem.save()
            else:
                citem.cqty=1
        else:
            messages.error(request,"product out of stock")
    return redirect(ditm)

def rmcart(request,id):
    data=cart.objects.get(pk=id)
    data.delete()
    return redirect(ditm)


def mlor(re):
    u=user.objects.get(uname=re.session['uid'])
    itm=cart.objects.filter(uid=u)
    return render(re,'mor.html',{'d':itm})

def buy(re):
    u=user.objects.get(uname=re.session['uid'])
    itm=cart.objects.filter(uid=u)
    for i in itm:
        itms=item.objects.get(pk=i.iid.pk)
        print(itms.iname)
    return render(re, 'mpay.html', {'j': u,'d':itm})

def mby(re):
    u = user.objects.get(uname=re.session['uid'])
    itm = cart.objects.filter(uid=u)
    tr=0
    if re.method == 'POST':
        adr = re.POST['ad']
        n = re.POST['ph']
        a = datetime.now().strftime("%Y-%m-%d")
        dt = datetime.now()
        year = dt.year
        month = dt.month
        day = dt.day
        day += 5
        d = datetime(year, month, day)
        dd = d.strftime("%Y-%m-%d")
        for i in itm:
            itms=item.objects.get(pk=i.iid.pk)
            data = order.objects.create(uid=u, iid=itms, tqty=i.cqty, oadrs=adr,ono=n,odate=a,ddate=dd,frate=i.trate)
            data.save()
            o = order.objects.filter(pk=i.iid.pk)
            itms.qty-=i.cqty
            itms.save()
            tr+=i.trate
            i.iid.prate=i.trate
            itm.delete()
        if tr>999:
            tr=int(tr*100)
        else:
            tr=int(tr*100)
        return render(re, 'razor.html',{'o':o,'t':tr})
    return render(re, 'mpay.html', {'j': u, 'd': itm})


def sorder(request,id):
    itm=item.objects.get(pk=id)
    if itm.qty>0:
        if itm.qty< 10:
                z = 'ayiraarts@gmail.com'
                email_message = f" The product {itm.iname} is falling out off stock. its only {itm.qty}, updatae fastly , its high on demand."
                send_mail('ALERT...UPDATE STOCK...', email_message, 'settings.EMAIL_HOST_USER', [z], fail_silently=False)
        itm.prate=itm.rate
        itm.pqty=1
        itm.save()
        return render(request,'sor.html',{'i':itm})
    else:
        msg="product out of stock"
        print(msg)
    return render(request,'sor.html',{'i':itm, 'm': msg})

def minusitm(re,id):
    if 'uid' in re.session:
        c=item.objects.get(iid=id)
        if c.qty > 1:
            if c.pqty>1:
                c.pqty= c.pqty - 1
                c.prate-=c.rate
                c.save()
            else:
                c.prate=c.rate
                c.pqty=1
                c.qty=c.qty
        else:
            messages.error(re, "product out of stock")
    return render(re,'sor.html',{'i':c})

# Increasing single items

def plusitm(re,id):
    if 'uid' in re.session:
        c=item.objects.get(iid=id)
        if c.qty>=1:
            c.pqty = c.pqty + 1
            c.prate=c.prate+c.rate
            c.save()
        else:
            messages.error(re, "product out of stock")
    return render(re,'sor.html',{'i':c})


def sby(re,id):
    itm=item.objects.get(iid=id)
    us = user.objects.get(uname=re.session['uid'])
    tr=0
    if itm.qty>0:
        if re.method=='POST':
            adr=re.POST['ad']
            n = re.POST['ph']
            itm.save()
            a=datetime.now().strftime("%Y-%m-%d")
            print(a)
            dt = datetime.now()
            year = dt.year
            month =dt.month
            day = dt.day
            day+=5
            d = datetime(year, month, day)
            dd=d.strftime("%Y-%m-%d")
            ord=order.objects.create(odate=a,ddate=dd,uid=us,iid=itm,oadrs=adr,ono=n,tqty=itm.pqty,frate=itm.prate)
            ord.save()
            o = order.objects.filter(iid=id)
            tr +=itm.prate
            if tr>999:
                tr=int(tr*100)
            else:
                tr=int(tr*100)
            itm.qty=itm.qty-itm.pqty
            itm.save()
        return render(re, 'razor.html', {'o': itm, 't': tr})
    else:
        messages.error(re,"product out of stock")

def aordtl(re):
    if 'aid' in re.session:
        o=order.objects.filter()
        return render(re,'aordr.html',{'ora':o})
    return redirect(log)

def ordtls(re):
    u=user.objects.get(uname=re.session['uid'])
    o=order.objects.filter(uid=u)
    return render(re,'ordered.html',{'ords':o})

def paymnt(re,id):
        us = user.objects.get(uname=re.session['uid'])
        it=item.objects.get(iid=id)
        return render(re, 'spay.html', {'j':us,'i':it})



def razor(request):
    if 'uid' in request.session:
        u = user.objects.get(uname=request.session['uid'])
        o = order.objects.get(uid=u)
        client = razorpay.Client(
                auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        # cursor = connection.cursor()
        # cursor.execute("update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(id) + "' ")
        payment = client.order.create({'amount':o, 'currency':'INR', 'payment_capture':'1'})
        return render(request, "razor.html",payment)


# def cancel(re,id):
#     o = order.objects.get(iid=id)
#     o.delete()
#     return redirect(ds)

def logoutu(request):
    if 'uid' in request.session:
        request.session.flush()
        return redirect(log)