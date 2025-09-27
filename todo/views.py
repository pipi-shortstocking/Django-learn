from django.shortcuts import render, redirect
from .models import Todo

def todo_list(request):
    todos = Todo.objects.filter(complete=False)
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = Todo.objects.get(id=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})