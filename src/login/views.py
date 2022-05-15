from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def register_user(request):
    form = CreateUserForm()
    print('aaya')
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            print('ok nro')
            return redirect('login')
        else:
            print('ni yaar')
    context = {
        'form':form
    }
    return render(request,'register.html',context=context)\

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, f'Logged in as: {username}')
            return redirect('home')
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')