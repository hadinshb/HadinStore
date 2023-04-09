from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
#ACTIVATION EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegistrationForm
from .models import Account


# Create your views here.
def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]

            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            #User Email Activation Sending
            current_site=get_current_site(request)
            mail_subject='Please Active Your Account...'
            email_messages=render_to_string('accounts/verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            email_to=email
            email_verification=EmailMessage(mail_subject,email_messages,to=[email_to])
            email_verification.send()
            return redirect("/accounts/login?command=verification&email="+email)

    else:
        form=RegistrationForm()
    context={'form':form}
    return render(request,'accounts/register.html',context)


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account.objects.get(pk=uid)
        
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
       user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations! Your account is now activated...')
        return redirect('login')
    else: 
        messages.error(request,'Invalid request...')
        return redirect('register')   


def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid login credentials .')
            return redirect('login')
        

    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out...')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            #User Email Password Reset Sending
            current_site=get_current_site(request)
            mail_subject='Reset Your Password...'
            email_messages=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            email_to=email
            email_verification=EmailMessage(mail_subject,email_messages,to=[email_to])
            email_verification.send()
            
            messages.success(request,'Password reset link has been sent to your email.')
            return redirect('login')
        else:
            messages.error(request,"User does not exist...")

    return render(request,'accounts/forgotPassword.html')



def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account.objects.get(pk=uid)
        
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
       user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please Reset your password...')
        return redirect('resetpassword')   
    
    else: 
        messages.error(request,'Invalid request...')
        return redirect('login')   
    

def resetpassword(request):
    if request.method == 'POST':
        password=request.POST['password']
        confirm_paswword=request.POST['confirm_password']

        if password == confirm_paswword:
            uid=request.session['uid']
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            del request.session['uid']
            messages.success(request,'Password has been changed successfully...')
            return redirect('login')
        else:
            messages.error(request,'Passwords does not match...')
            return  redirect('resetpassword')
    else:
        if 'uid' not in request.session:
            return redirect('login')
    return render(request,'accounts/reset_password.html')