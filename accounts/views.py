from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#ACTIVATION EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            # messages.success(request,'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request,'Invalid login credentials .')
            return redirect('login')
        

    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out...')
    return redirect('login')
