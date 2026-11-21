from django.shortcuts import render,redirect
def hello(request):
    return render(request,'accounts/demo.html')