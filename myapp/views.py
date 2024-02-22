from django.shortcuts import render,redirect
from django import forms
from myapp.models import Todo
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache

# Create your views here.


def signin_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

desc=[signin_required,never_cache]
#form of todo
class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        exclude=("created_date","user_objects")
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "status":forms.Select(attrs={"class":"form-control form-select"})
        }



# registrationform
class Registrationform(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }



# login
class SigninForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))




# todo list    
@method_decorator(desc,name="dispatch")     
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(user_objects=request.user)
        return render(request,"todo_list.html",{"data":qs})
    
# todo creating
@method_decorator(desc,name="dispatch")     
class TodocreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            # data=form.cleaned_data
            # user_objects=request.user
            # TodoForm.objects.create(**data,user_objects)
            form.instance.user_objects=request.user
            form.save()
            messages.success(request,"todo added")
            return redirect("todo-list")
        else:
            messages.error(request,"todo adding failed")
            return render(request,"todo_add.html",{"form":form})

# todo detail
@method_decorator(desc,name="dispatch")     
class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        return render(request,"todo_detail.html",{"data":qs})


# delete view
@method_decorator(desc,name="dispatch")     
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.get(id=id).delete()
        messages.success(request,"todo deleted")
        return redirect("todo-list")
    


# update view
@method_decorator(desc,name="dispatch")     
class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_objects=Todo.objects.get(id=id)
        form=TodoForm(instance=todo_objects)
        return render(request,"todo_update.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_objects=Todo.objects.get(id=id)
        form=TodoForm(request.POST,instance=todo_objects)
        if form.is_valid():
            form.save()
            messages.success(request,"todo updated")
            return redirect("todo-list")
        else:
            return render(request,"todo_update.html",{"form":form})

# signupview
# localhost:8000/signup/
# method get post
        
class SignupView(View):
    def get(self,request,*args,**kwargs):
        form=Registrationform()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=Registrationform(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("signin")
        else:
            return render(request,"login.html",{"form":form})



# signinview
# localhost:8000/signin/
# method get, post
        
class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=SigninForm()
        return render(request,"Login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=SigninForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                print("credentials are valid")
                login(request,user_object)
                return redirect("todo-list")
        print("invalid")
        return render(request,"Login.html",{"form":form})


# signout view
@method_decorator(desc,name="dispatch")     
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")