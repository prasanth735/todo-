from django.shortcuts import render,redirect
from django import forms
from myapp.models import Todo
from django.views.generic import View

# Create your views here.

#         form of todo

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        exclude=("created_date",)


#       todo list 
        

class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.all()
        return render(request,"todo_list.html",{"data":qs})
    
#         todo creating
class TodocreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todo-list")
        else:
         return render(request,"todo_add.html",{"form":form})

#         todo detail

class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        return render(request,"todo_detail.html",{"data":qs})


#          delete view
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.get(id=id).delete()
        return redirect("todo-list")
    


#       update view

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
            return redirect("todo-list")
        else:
            return render(request,"todo_update.html",{"form":form})
