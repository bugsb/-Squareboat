from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


def register_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="User Registration Success")
            return redirect('login')
        else:
            messages.success(request, message="User Registration Failed")
    context = {
        'form':form
    }
    return render(request,'register.html',context=context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, message=f'Logged in as: {username}')
            return redirect('home')
        else:
            messages.success(request, message="Invalid Credentials")

    return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, message=f"Logged out Successfully")
    return redirect('login')